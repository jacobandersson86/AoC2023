import re
import math

def initiate_inputs(rack, outputs) :
    inputs = dict()
    for module in rack :
        _, name, _ = rack[module]
        input_names = []
        # Find all outputs that refers to my module
        for out in outputs :
            _, input_name, output = rack[out]
            if name in set(output) :
                input_names.append(input_name)
        inputs[name] = input_names
    return inputs

def initiate_outputs(rack) :
    outputs = dict()

    for module in rack :
        _, name, _ = rack[module]
        outputs[name] = 0

    return outputs

def process_pulse(pulse, to, rack, inputs, outputs):
    new_pulse = []

    if to not in rack:
        return []

    operator, _, connections = rack[to]

    new_pulse = False
    match operator :
        case '&' :
            new_pulse = True
                # Check states
            input_names =  inputs[to]
            if len(input_names) != 0 :
                input_states = [outputs[name] for name in input_names if name in outputs]
            if all([state == 1 for state in input_states]) :
                outputs[to] = 0
            else :
                outputs[to] = 1
        case '%' :
            if pulse == 0 :
                outputs[to] = (outputs[to] + 1) % 2
                new_pulse = True
        case None :
            outputs[to] = pulse
            new_pulse = True

    next_pulses = []
    if new_pulse :
        for connection in connections:
            next_pulses.append((outputs[to], connection))

    return next_pulses

def read_data(file) :
    with open(file) as f :
        lines = f.readlines()

    pattern = re.compile(r'(%|&)(\w+)')

    rack = dict()
    for line in lines :
        gate, outputs = line.strip('\n').split(' -> ')

        outputs = re.findall('[a-z]+', outputs)

        if gate == 'broadcaster' :
            op = None
            name = 'broadcaster'
        else :
            match = pattern.match(gate)
            op, name = match.groups()

        rack[name] = (op, name, outputs)

    return rack

def find_flippeliflops(head, rack, inputs) :
    # Find inputs check attach to head
    head_inputs = inputs[head]

    # For each input check if is a flip flop
    found = []
    next_input = []
    for input in head_inputs :
        op ,_ ,_  = rack[input]
        if op == '%' :
            found.append(input)
        else :
            next_input.append(input)

    # False, go deeper.
    for input in next_input :
        found_upstream = find_flippeliflops(input, rack, inputs)
        found.extend(found_upstream)

    # True return name of flip flop
    return list(set(found))

def find_connections(head, rack, inputs, depth) :
    depth -= 1

    head_inputs = inputs[head]
    found = []
    if depth > 0 :
        for input in head_inputs :
            found_upstream = find_connections(input, rack, inputs, depth)
            found.extend(found_upstream)

        return list(set(found))
    else :
        return head_inputs


def find_periods(gates, outputs, periods, n) :
    all_found = True
    for gate in gates :
        last, n_last, period, n_period, first = periods[gate]
        now = outputs[gate]

        if last == 0 and now == 1:
            if first == 0 :
                first = n
            if period[-1] < 0 :
                period[-1] += 1
            else :
                this_period = n - n_last
                if period[-1] == this_period:
                    n_period[-1] += 1
                else :
                    period.append(this_period)
                    n_period.append(1)
            n_last = n

        last = now
        periods[gate] = (last, n_last, period, n_period, first)

        if period[-1] <= 0 :
            all_found = False
    return periods, all_found

def main():
    n_high_pulses = 0
    n_low_pulse = 0

    # rack = example2
    rack = read_data('day20/input')

    outputs = initiate_outputs(rack)
    inputs = initiate_inputs(rack, outputs)

    n_push = 1000
    for _ in range(n_push) :
        pulse_queue = [(0, 'broadcaster')]

        while len(pulse_queue) :
            pulse = pulse_queue.pop(0)
            state, reciptent = pulse

            if state :
                n_high_pulses += 1
            else :
                n_low_pulse += 1

            new_pulses = process_pulse(state, reciptent, rack, inputs, outputs)
            pulse_queue.extend(new_pulses)

    print(f"High {n_high_pulses} Low {n_low_pulse}")
    print(f"Part 1 : {n_high_pulses * n_low_pulse}", end='\n\n')

    # Add rx to outputs (in order to search inputs attached to it)
    rack['rx'] = (None, 'rx', [])

    # Reset Outputs
    outputs = initiate_outputs(rack)
    inputs = initiate_inputs(rack, outputs)

    # Find gates attached to rx
    heads = find_connections('rx', rack, inputs, 3)
    print(f"Interesting gates: {heads}")

    rack.pop('rx')

    largest_periods = []
    for head in heads :
        print(f"Explore {head}")
        flip_flops = find_flippeliflops(head, rack, inputs)
        # Reset Outputs
        outputs = initiate_outputs(rack)
        inputs = initiate_inputs(rack, outputs)

        # Find periodicity of those
        periods = dict()
        for f in flip_flops :
            periods[f] = (0, 0, [-3], [0], 0)

        all_found = False
        n = 0
        while not all_found :
            pulse_queue = [(0, 'broadcaster')]

            while len(pulse_queue) :
                pulse = pulse_queue.pop(0)
                state, reciptent = pulse
                new_pulses = process_pulse(state, reciptent, rack, inputs, outputs)
                pulse_queue.extend(new_pulses)

            periods, all_found = find_periods(flip_flops, outputs, periods, n)
            n += 1

        for p in periods:
            print(p, periods[p])
        n -= 1
        # Throw LCM at it
        periods = [(periods[item][2]) for item in periods]

        largest = sorted(periods)[-1][-1]
        print(f"Largest periods: {largest}")
        largest_periods.append(largest)
        print("")

    # Find when all heads are 1 at the same time
    least = math.lcm(*largest_periods)
    print(f"Part 2 {least}")

if __name__ == '__main__' :
    main()
