import re
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

example1 = {
    'broadcaster' : (None, 'broadcaster', ['a', 'b', 'c']),
    'a' :       ('%', 'a', ['b']),
    'b' :       ('%', 'b', ['c']),
    'c' :       ('%', 'c', ['inv']),
    'inv':      ('&', 'inv', ['a']),
}

example2 = {
    'broadcaster'   : (None, 'broadcaster', ['a']),
    'a'             : ('%', 'a', ['inv', 'con']),
    'inv'           : ('&', 'inv', ['b']),
    'b'             : ('%', 'b', ['con']),
    'con'           : ('&', 'con', ['output']),
    'output'        : (None, 'output', [])
}

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
                input_states = [outputs[name] for name in input_names]
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
        # The push of the button doesn't count.

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
    print(f"Part 1 : {n_high_pulses * n_low_pulse}")

if __name__ == '__main__' :
    main()
