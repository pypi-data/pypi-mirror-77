"""Update project metrics on The Coverage Space.

Usage:
  coveragespace <owner/repo> <metric> [<value>] [--verbose] [--exit-code]
  coveragespace <owner/repo> --reset [--verbose]
  coveragespace (-h | --help)
  coveragespace (-V | --version)

Options:
  -h --help         Show this help screen.
  -V --version      Show the program version.
  -v --verbose      Always display the coverage metrics.
  -x --exit-code    Return non-zero exit code on failures.

"""


import json
import sys
from shutil import get_terminal_size

import colorama
import log
from docopt import DocoptExit, docopt

from . import API, VERSION, client, services
from .plugins import get_coverage, launch_report


def main():
    """Parse command-line arguments, configure logging, and run the program."""
    colorama.init(autoreset=True)
    arguments = docopt(__doc__, version=VERSION)

    slug = arguments['<owner/repo>']
    metric = arguments['<metric>']
    reset = arguments['--reset']
    value = arguments['<value>']
    verbose = arguments['--verbose']
    hardfail = arguments['--exit-code']

    log.reset()
    log.init(level=log.DEBUG if verbose else log.WARNING)

    if '/' not in slug:
        raise DocoptExit("<owner/repo> slug must contain a slash" + '\n')

    success = run(slug, metric, value, reset, verbose, hardfail)

    if not success and hardfail:
        sys.exit(1)


def run(*args, **kwargs):
    """Run the program."""
    if services.detected():
        log.info("Coverage check skipped when running on CI service")
        return True

    return call(*args, **kwargs)


def call(slug, metric, value, reset=False, verbose=False, hardfail=False):
    """Call the API and display errors."""
    url = "{}/{}".format(API, slug)
    if reset:
        data = {metric: None}
        response = client.delete(url, data)
    else:
        data = {metric: value or get_coverage()}
        response = client.get(url, data)

    if response.status_code == 200:
        if verbose:
            display("coverage increased", response.json(), colorama.Fore.GREEN)
        return True

    if response.status_code == 202:
        display("coverage reset", response.json(), colorama.Fore.BLUE)
        return True

    if response.status_code == 422:
        color = colorama.Fore.RED if hardfail else colorama.Fore.YELLOW
        data = response.json()
        message = "To reset metrics, run: ^coveragespace {} --reset$".format(slug)
        data['help'] = message  # type: ignore
        display("coverage decreased", data, color)
        launch_report()
        return False

    try:
        data = response.json()
        display("coverage unknown", data, colorama.Fore.RED)
    except (TypeError, ValueError) as exc:
        data = response.data.decode('utf-8')
        log.error("%s\n\nwhen decoding response:\n\n%s\n", exc, data)
    return False


def display(title, data, color=""):
    """Write colored text to the console."""
    color += colorama.Style.BRIGHT
    width, _ = get_terminal_size()
    print(color + "{0:=^{1}}".format(' ' + title + ' ', width))
    message = json.dumps(data, indent=4)
    message = message.replace('^', colorama.Fore.WHITE + colorama.Style.BRIGHT)
    message = message.replace('$', colorama.Style.RESET_ALL)
    print(message)
    print(color + '=' * width)
