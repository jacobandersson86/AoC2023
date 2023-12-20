
def process(module, rack, inputs, outputs) :
    operator, name, out = rack[module]

    # Check states
    input_names =  inputs[name]
    if len(input_names) != 0 :
        input_states, last_input_state = zip(*[outputs[name] for name in input_names])
    else:
        input_states, last_input_state = [], []
    output_state, _ = outputs[name]

    # Check operation

    process_output = 0
    match operator :
        case '&' :
            if all([state == 1 for state in last_input_state]) :
                process_output = 1
        case '%' :
            if all([state == 0 for state in input_states]):
                process_output = (output_state + 1) % 2
        case None :
            if len(input_names) != 0: # Broadcaster
                process_output = input_states[0]
            else : # Button
                process_output = 1
    # Update outputs
    outputs[name] = (process_output, output_state)

    # A pulse is when we changed state
    if process_output == output_state :
        out = []

    return out, process_output

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
        outputs[name] = (0, 0)

    return outputs


example1 = {
    'button' :  (None, "button", ["broadcaster"]),
    'broadcaster' : (None, 'broadcaster', ['a', 'b', 'c']),
    'a' :       ('%', 'a', ['b']),
    'b' :       ('%', 'b', ['c']),
    'c' :       ('%', 'c', ['inv']),
    'inv':      ('&', 'inv', ['a']),
}

def process_loop(module_queue, rack, inputs, outputs, count) :
    slots = module_queue.pop(0)
    for module in slots :
        next_modules, pulse = process(module, rack, inputs, outputs)
        module_queue.append(next_modules)

        high, low = count
        if pulse :
            high += 1
        else :
            low += 1

    return high, low


def main():
    n_high_pulses = 0
    n_low_pulse = 0

    rack = example1

    module_queue = [["button"]]

    outputs = initiate_outputs(rack)
    inputs = initiate_inputs(rack, outputs)
    outputs['button'] = (1, 0)

    # pulse = process_loop(module_queue, rack, inputs, outputs)

    # if pulse :
    #     n_high_pulses += 1
    # else :
    #     n_low_pulse += 1

    count = (n_high_pulses, n_low_pulse)

    for _ in range(12) :
        count = process_loop(module_queue, rack, inputs, outputs, count)

        if all([outputs[name][0] == 0 for name in outputs]) :
            # Initial state!
            break

    n_high_pulses, n_low_pulse = count
    print(f"High {n_high_pulses} Low {n_low_pulse}")


if __name__ == '__main__' :
    main()
