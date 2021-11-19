import json
import re
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
from typing import Dict


@dataclass
class BusStop:
    id: int
    next_stop: int
    a_time: int
    stop_name: str
    type: str = ""


class BusChecker:
    def __init__(self, easy_rider_data: list, field_requirements=None):
        self.field_requirements = field_requirements or {
            "bus_id": {"type": int, "required": True, "format": self.is_positive},
            "stop_id": {"type": int, "required": True, "format": self.is_positive},
            "stop_name": {"type": str, "required": True, "format": self.is_stop_name},
            "next_stop": {"type": int, "required": True, "format": self.is_positive},
            "stop_type": {"type": str, "required": False, "format": self.is_stop_type},
            "a_time": {"type": str, "required": True, "format": self.is_time_format},
        }
        self.easy_rider_data = easy_rider_data
        self.error_counter = Counter()
        self.lines = self.reformat_easy_rider_data()

    def reformat_easy_rider_data(self):
        lines = {}
        for bus_info in self.easy_rider_data:
            if bus_info["bus_id"] not in lines:
                lines[bus_info["bus_id"]] = {"stops": {},
                                             "time_error": None}
            hours, minutes = map(int, bus_info["a_time"].split(":"))
            bus_stop = BusStop(
                id=bus_info["stop_id"],
                stop_name=bus_info["stop_name"],
                next_stop=bus_info["next_stop"],
                a_time=hours * 60 + minutes,
                type=bus_info["stop_type"]
            )
            if bus_info["stop_type"] == "S":
                lines[bus_info["bus_id"]]["start"] = bus_stop.id
            lines[bus_info["bus_id"]]["stops"][bus_stop.id] = bus_stop
        return lines

    def arrival_time_check(self):
        lines = self.lines
        for line in lines:

            current_id = lines[line]["start"]
            current_stop = lines[line]["stops"][current_id]
            next_id = current_stop.next_stop

            while next_id != 0:
                check_time = current_stop.a_time < lines[line]["stops"][next_id].a_time
                if not check_time:
                    line_name = lines[line]["stops"][next_id].stop_name
                    lines[line][
                        "time_error"] = f"bus_id line {line}: wrong time on station {line_name}"
                    break
                current_stop = lines[line]["stops"][next_id]
                next_id = current_stop.next_stop
        errors = [lines[line]["time_error"] for line in lines if lines[line]["time_error"]]
        if errors:
            return '\n'.join(("Arrival time test:", *errors))
        else:
            return "\n".join(("Arrival time test:", "OK"))

    def check_lines(self) -> str:
        lines: dict = {}
        stops: Dict[str, set] = {
            'start_stops': set(),
            'transfer_stops': set(),
            'finish_stops': set(),
        }
        for bus_info in self.easy_rider_data:

            if bus_info["bus_id"] not in lines:
                lines[bus_info["bus_id"]] = {"all_stops": set()}
            lines[bus_info["bus_id"]]["all_stops"].add(bus_info["stop_name"])

            if bus_info["stop_type"] == "S":
                stops['start_stops'].add(bus_info["stop_name"])
                lines[bus_info["bus_id"]]["start"] = bus_info["stop_name"]
            elif bus_info["stop_type"] == "F":
                stops['finish_stops'].add(bus_info["stop_name"])
                lines[bus_info["bus_id"]]["finish"] = bus_info["stop_name"]

        for line in lines:
            if not (lines[line].get("start") and lines[line].get("finish")):
                return f"There is no start or end stop for the line: {line}"

        for line1, line2 in combinations(lines, r=2):
            stops['transfer_stops'] |= lines[line1]["all_stops"] & lines[line2]["all_stops"]

        return stops

    def check_on_demand_stops(self):
        stops = self.check_lines()
        should_check_stops = stops["start_stops"] | stops["transfer_stops"] | stops["finish_stops"]
        on_demand_stops = set()
        for line in self.lines:
            for stop_id, stop in self.lines[line]['stops'].items():
                if stop.type == "O":
                    on_demand_stops.add(stop.stop_name)
        return sorted(list(on_demand_stops.intersection(should_check_stops)))

    def print_result_on_demand_check(self):
        on_demand_stops_errors = self.check_on_demand_stops()
        result = "On demand stops test:"
        if on_demand_stops_errors:
            print("\n".join((
                result,
                f"Wrong stop type: {on_demand_stops_errors}"
            )))
        else:
            print("\n".join((
                result,
                "OK"
            )))

    def print_check_lines_result(self):
        stops = self.check_lines()
        result = '\n'.join(
            (f'Start stops: {len(stops["start_stops"])} {sorted(stops["start_stops"])}',
             f'Transfer stops: {len(stops["transfer_stops"])} {sorted(stops["transfer_stops"])}',
             f'Finish stops: {len(stops["finish_stops"])} {sorted(stops["finish_stops"])}'))
        print(result)

    def count_stops(self):
        unique = {}
        for bus_info in self.easy_rider_data:
            if bus_info["bus_id"] not in unique:
                unique[bus_info["bus_id"]] = set()
            unique[bus_info["bus_id"]].add(bus_info["stop_name"])
        return {bus_id: len(unique[bus_id]) for bus_id in unique}

    def print_stops(self):
        print("Line names and number of stops:")
        stops_info = self.count_stops()
        for bus_id in sorted(stops_info):
            print(f'bus_id: {bus_id}, stops: {stops_info[bus_id]}')

    def print_errors(self):
        self.easy_rider_check()
        print(f"Type and required field validation: {sum(self.error_counter.values())} errors")
        order = ["stop_name", "stop_type", "a_time"]
        for field in order:
            print(f"{field}: {self.error_counter[field]}")

    def easy_rider_check(self):
        for row in self.easy_rider_data:
            self.row_check(row)
        return self.error_counter

    def row_check(self, row):
        for field in self.field_requirements:
            if not isinstance(row[field], self.field_requirements[field]["type"]):
                self.error_counter[field] += 1
                continue

            elif not self.field_requirements[field]["format"](row[field]):
                self.error_counter[field] += 1

            elif self.field_requirements[field]['required'] and row[field] is None:
                self.error_counter[field] += 1
                continue

    def is_stop_name(self, value):
        if not (type(value) == str and bool(value)):
            return False
        words = value.split()
        if len(words) < 2:
            return False
        if not words[0][0].isupper() or words[-1] not in ("Road", "Avenue", "Street", "Boulevard"):
            return False
        return True

    def is_stop_type(self, stop):
        return stop in ("S", "O", "F") or stop == ""

    def is_positive(self, value: int) -> bool:
        return value >= 0

    def is_time_format(self, s: str) -> bool:
        time_re = re.compile(r'^(([01]\d|2[0-3]):([0-5]\d)|24:00)$')
        return bool(time_re.match(s))


def main():
    # with open("test.json", encoding="utf-8") as file:
    #     buses = json.load(file)
    buses = json.loads(input())
    bus_checker = BusChecker(easy_rider_data=buses)
    bus_checker.print_result_on_demand_check()


if __name__ == '__main__':
    main()
