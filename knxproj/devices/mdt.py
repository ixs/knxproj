"""Container for MDT devices."""
# pylint: disable=too-many-locals

import logging
import re

import attr

from .devices import Switch


@attr.s
class GT2(Switch):
    """MDT Glastaster 2."""

    texts = attr.ib(factory=list)

    line0_re = re.compile(
        r"^(?P<nr>T1|T2|T1/2)(\s?(?P<duration>kurz|lang))?:\s(?P<description>.*)$"
    )
    line1_re = re.compile(
        r"^(?P<nr>T3|T4|T3/4)(\s?(?P<duration>kurz|lang))?:\s(?P<description>.*)$"
    )
    line2_re = re.compile(
        r"^(?P<nr>T5|T6|T5/6)(\s?(?P<duration>kurz|lang))?:\s(?P<description>.*)$"
    )
    line3_re = re.compile(
        r"^(?P<nr>T7|T8|T7/8)(\s?(?P<duration>kurz|lang))?:\s(?P<description>.*)$"
    )
    line4_re = re.compile(
        r"^(?P<nr>T9|T10|T9/10)(\s?(?P<duration>kurz|lang))?:\s(?P<description>.*)$"
    )
    line5_re = re.compile(
        r"^(?P<nr>T11|T12|T11/12)(\s?(?P<duration>kurz|lang))?:\s(?P<description>.*)$"
    )

    status_re = re.compile(r"^(?P<description>(Statustext|Meldung)\s.+)$")
    led_re = re.compile(r"^LED\s(?P<description>.*)$")

    @classmethod
    def from_device(cls, device, *args, **kwargs):
        """Create a MDT Glastaster 2 from a generic device."""

        return cls(texts=kwargs["texts"], **vars(device))

    def doc(self):
        """Show all pages from a GT2."""

        def _match_line(lines: set, expr) -> str:
            sep = 5 * " "
            result = []
            for line in lines.copy():
                match = expr.match(line)

                if match is None:
                    continue

                lines.remove(line)

                description = match.group("description").strip()

                result.append(description)
            return sep.join(result)

        # Match the lines of the text
        lines = set(self.texts)

        # TODO: Switch w.r.t. layout
        line0 = [_match_line(lines, self.line0_re), _match_line(lines, self.line3_re)]
        line1 = [_match_line(lines, self.line1_re), _match_line(lines, self.line4_re)]
        line2 = [_match_line(lines, self.line2_re), _match_line(lines, self.line5_re)]

        # TODO: document status / LED
        line_status = _match_line(lines, self.status_re)
        line_led = _match_line(lines, self.led_re)
        if line_status or line_led:
            logging.info("%s has led and/or status message activated.", self.name)

        # Assert there are no leftovers
        if lines:
            raise Exception(lines)

        # Formatting
        width = max(map(len, [line0, line1, line2]))
        width = 50
        button_l = "|    | "
        button_r = " |    |"
        hline = (width + len(button_l) + len(button_r)) * "="
        hline_small = len(hline) * "-"

        # Count pages
        def page_count_fcn(line_x):
            return len([x for x in line_x if x])

        page_count = max(map(page_count_fcn, (line0, line1, line2)))

        # Create pages
        for idx in range(page_count):
            name = f"{self.name} {idx+1}/{page_count}"
            switch = f"""
{name}
{hline}
{button_l}{line0[idx].center(width)}{button_r}
{hline_small}
{button_l}{line1[idx].center(width)}{button_r}
{hline_small}
{button_l}{line2[idx].center(width)}{button_r}
{hline}
"""
            print(switch)
