import synacell.cmodule
import synacell.signal as signal
import matplotlib.pyplot as plt
import math
import numpy as np


def plot_CellEMA() -> (int, str):
    """
    Test CellEMA and CellIntegrator

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=123.0, amp=1000.0, phase=0.0)
    sin2 = signal.func_generator(func_name="sin", freq=246.0, amp=2000.0, phase=0.0)
    sin3 = signal.func_generator(func_name="sin", freq=173.0, amp=1347.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin2_arr = signal.func_to_nparray(func=sin2, t_min=0.5, t_max=1.0)
    sin3_arr = signal.func_to_nparray(func=sin3, t_min=0.3, t_max=1.0)
    signal.make_wav(sin1_arr + sin2_arr + sin3_arr, "./CellEMA.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./CellEMA.wav")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.add_part("id=1,type=CellValve,ofs=0,opn=5,cls=23")
    net.add_part("id=1001,type=SynaBuffer,ciid=0,coid=2")
    net.add_part("id=2,type=CellValve,ofs=0,opn=7,cls=14")
    net.add_part("id=1002,type=SynaBuffer,ciid=1,coid=3")
    net.add_part("id=1003,type=SynaBuffer,ciid=2,coid=3")
    net.add_part("id=3,type=CellBuffer")
    net.add_part("id=1004,type=SynaRCA,ciid=1,coid=4")
    net.add_part("id=1005,type=SynaRCA,ciid=2,coid=4")
    net.add_part("id=4,type=CellBuffer")
    net.add_part("id=1006,type=SynaRCA,ciid=1,coid=5")
    net.add_part("id=1007,type=SynaRCA,ciid=2,coid=5")
    net.add_part("id=5,type=CellIntegrator")
    net.add_part("id=1008,type=SynaRCA,ciid=1,coid=6")
    net.add_part("id=1009,type=SynaRCA,ciid=2,coid=6")
    net.add_part("id=6,type=CellEMA,alpha=0.1")
    net.add_part("id=1010,type=SynaRCA,ciid=1,coid=7")
    net.add_part("id=1011,type=SynaRCA,ciid=2,coid=7")
    net.add_part("id=7,type=CellEMA,alpha=0.9")
    net.add_part("id=1012,type=SynaBuffer,ciid=5,coid=8")
    net.add_part("id=8,type=CellEMA,alpha=0.02")
    net.add_part("id=1013,type=SynaBuffer,ciid=5,coid=9")
    net.add_part("id=9,type=CellEMA,alpha=0.002")

    net.connect_syna()
    net.set_recorder("id=0,pid=0,value=vo,beg=0,size=10000")
    net.set_recorder("id=1,pid=1,value=vi,beg=0,size=10000")
    net.set_recorder("id=2,pid=1,value=vo,beg=0,size=10000")
    net.set_recorder("id=3,pid=2,value=vo,beg=0,size=10000")
    net.set_recorder("id=4,pid=3,value=vi,beg=0,size=10000")
    net.set_recorder("id=5,pid=4,value=vi,beg=0,size=10000")
    net.set_recorder("id=6,pid=5,value=vo,beg=0,size=10000")
    net.set_recorder("id=7,pid=6,value=vo,beg=0,size=10000")
    net.set_recorder("id=8,pid=7,value=vo,beg=0,size=10000")
    net.set_recorder("id=9,pid=8,value=vo,beg=0,size=10000")
    net.set_recorder("id=10,pid=9,value=vo,beg=0,size=10000")

    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record = [
        net.get_record(0),
        net.get_record(1),
        net.get_record(2),
        net.get_record(3),
        net.get_record(4),
        net.get_record(5),
        net.get_record(6),
        net.get_record(7),
        net.get_record(8),
        net.get_record(9),
        net.get_record(10),
    ]

    fig, ax = plt.subplots(3, 1, sharex='col')
    fig.suptitle('CellIntegrator test')
    # plot 1
    ax[0].plot([i * 1.0 / 16000.0 for i in record[0].pc], record[0].data, '-', label="input signal")
    ax[0].plot([i * 1.0 / 16000.0 for i in record[4].pc], record[4].data, '--',
               label="valve 1 + valve 2")
    ax[0].grid(True)
    ax[0].legend()

    # plot 2
    ax[1].plot([i * 1.0 / 16000.0 for i in record[5].pc], record[5].data*10, '-',
               label="valve 1 + valve 2 -> buffer (SynaRCA)")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[6].pc], record[6].data, '.-',
               label="valve 1 + valve 2 -> integrator (SynaRCA)")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[7].pc], record[7].data, '-',
               label="valve 1 + valve 2 -> ema 1.0 (SynaRCA)")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[8].pc], record[8].data, '-',
               label="valve 1 + valve 2 -> ema 0.5 (SynaRCA)")
    ax[1].grid(True)
    ax[1].legend()

    # plot 3
    ax[2].plot([i * 1.0 / 16000.0 for i in record[9].pc], record[9].data, '-',
               label="integrator -> ema 0.02 (SynaBuffer)")
    ax[2].plot([i * 1.0 / 16000.0 for i in record[10].pc], record[10].data, '-',
               label="integrator -> ema 0.002 (SynaBuffer)")
    ax[2].grid(True)
    ax[2].legend()

    plt.xlabel("Time [s]")
    plt.show()

    return 0, "Success"


def plot_CellEMA_sum() -> (int, str):
    """
    Test CellEMA with sum=2

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    # Generate wav file
    amp = 300
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=200.0, amp=amp, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.05, t_max=0.25, fixed_size=True)
    signal.make_wav(sin1_arr, "./CellEMA_sum.wav")

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellData,file=./CellEMA_sum.wav")
    net.add_part("id=1000,type=SynaBuffer,ciid=0,coid=1")
    net.add_part("id=1,type=CellEMA,alpha=0.02,sum=2")
    net.add_part("id=1001,type=SynaBuffer,ciid=0,coid=2")
    net.add_part("id=2,type=CellEMA,alpha=0.002,sum=2")

    net.connect_syna()
    net.set_recorder("id=0,pid=0,value=vo,beg=0,size=8000")
    net.set_recorder("id=1,pid=1,value=vo,beg=0,size=8000")
    net.set_recorder("id=2,pid=2,value=vo,beg=0,size=8000")

    net.reset()
    net.run(8000, 1.0 / 16000.0)
    record = [
        net.get_record(0),
        net.get_record(1),
        net.get_record(2)
    ]

    fig, ax = plt.subplots(2, 1, sharex='col')
    fig.suptitle('CellEMA sum=2 test')
    # plot 1
    ax[0].plot([i * 1.0 / 16000.0 for i in record[0].pc], record[0].data, '-', label="input signal")
    ax[0].grid(True)
    ax[0].legend()

    # plot 2
    ax[1].plot([i * 1.0 / 16000.0 for i in record[1].pc], record[1].data, '-',
               label="CellEMA alpha=0.02")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[2].pc], record[2].data, '-',
               label="CellEMA alpha=0.002")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[1].pc],
               [(amp/math.sqrt(2))**2 for i in record[1].pc], '-', label="Effective power Veff^2")
    ax[1].grid(True)
    ax[1].legend()

    plt.xlabel("Time [s]")
    plt.show()


def plot_CellMultiData() -> (int, str):
    """
    Test CellMulitData

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    # Generate wav file
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=100.0, amp=1000.0, phase=0.0)
    sin2 = signal.func_generator(func_name="sin", freq=10.0, amp=1000.0, phase=0.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin2_arr = signal.func_to_nparray(func=sin2, t_min=0.0, t_max=1.0)
    signal.make_wav(sin1_arr, "./CellMultiData_100Hz.wav")
    signal.make_wav(sin2_arr, "./CellMultiData_10Hz.wav")

    # Single file loading
    api = synacell.cmodule.SnnAPI
    net1 = api.new_net()
    net1.add_part("id=0,type=CellData,file=./CellMultiData_100Hz.wav")
    net1.connect_syna()
    net1.set_recorder("id=0,pid=0,value=vo,beg=0,size=16000")
    net1.reset()
    net1.run(16000, 1.0 / 16000.0)
    record1 = net1.get_record(0)
    # Load another file
    net1.set_params(0, "file=./CellMultiData_10Hz.wav")
    net1.reset()
    net1.run(16000, 1.0 / 16000.0)
    record2 = net1.get_record(0)

    # Multi data, one from file other directly from data
    net2 = api.new_net()
    net2.add_part("id=0,type=CellMultiData")
    net2.set_params(0, "fid=0,file=./CellMultiData_100Hz.wav")
    net2.set_params_dbarr(0, f"fid=1,size={sin2_arr.shape[0]}", sin2_arr)
    net2.set_recorder("id=0,pid=0,value=vo,beg=0,size=16000")
    net2.connect_syna()
    net2.set_params(0, "selid=0")
    net2.reset()
    net2.run(16000, 1.0 / 16000.0)
    record3 = net2.get_record(0)
    net2.set_params(0, "selid=1")
    net2.reset()
    net2.run(16000, 1.0 / 16000.0)
    record4 = net2.get_record(0)

    fig, ax = plt.subplots(2, 1, sharex='col')
    fig.suptitle('CellMultiData test')

    # plot 1
    ax[0].plot([i * 1.0 / 16000.0 for i in record1.pc], record1.data, '-',
               label="CellData 100Hz")
    ax[0].plot([i * 1.0 / 16000.0 for i in record2.pc], record2.data, '-',
               label="CellData 10Hz")
    ax[0].grid(True)
    ax[0].legend()

    # plot 2
    ax[1].plot([i * 1.0 / 16000.0 for i in record3.pc], record3.data, '-',
               label="CellMultiData 100Hz (from file)")
    ax[1].plot([i * 1.0 / 16000.0 for i in record4.pc], record4.data, '-',
               label="CellMultiData 10Hz (from nparray)")
    ax[1].grid(True)
    ax[1].legend()

    plt.xlabel("Time [s]")
    plt.show()

    return 0, "Success"


def plot_CellMultiData_validate() -> (int, str):
    """
    Test CellMulitData used as validator

    :return: (int, str) 0 is success, everything else is error, str is mesage
    """

    # Generate two wav files and two validators
    signal = synacell.signal
    sin1 = signal.func_generator(func_name="sin", freq=100.0, amp=1000.0, phase=0.0)
    sin2 = signal.func_generator(func_name="sin", freq=300.0, amp=500.0, phase=0.0)
    const1 = signal.func_generator(func_name="const", amp=1000.0)
    const2 = signal.func_generator(func_name="const", amp=500.0)
    sin1_arr = signal.func_to_nparray(func=sin1, t_min=0.0, t_max=1.0)
    sin2_arr = signal.func_to_nparray(func=sin2, t_min=0.0, t_max=1.0)
    const1_arr = signal.func_to_nparray(func=const1, t_min=0.0, t_max=1.0)
    const2_arr = signal.func_to_nparray(func=const2, t_min=0.0, t_max=1.0)
    signal.make_wav(sin1_arr, "./CellMultiData_100Hz.wav")
    signal.make_wav(sin2_arr, "./CellMultiData_300Hz.wav")
    signal.make_wav(const1_arr, "./CellMultiData_valid_100Hz.wav")
    signal.make_wav(const2_arr, "./CellMultiData_valid_300Hz.wav")

    # Multi data and multi error
    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellMultiData")
    net.set_params(0, "fid=0,file=./CellMultiData_100Hz.wav")
    net.set_params(0, "fid=1,file=./CellMultiData_300Hz.wav")
    net.add_part("id=1,type=CellMultiData,validate=1")
    net.set_params(1, "fid=0,file=./CellMultiData_valid_100Hz.wav")
    net.set_params(1, "fid=1,file=./CellMultiData_valid_300Hz.wav")
    net.add_part("id=1000,type=SynaRCA,ciid=0,coid=1")
    net.set_recorder("id=0,pid=0,value=vo,beg=0,size=16000")
    net.set_recorder("id=1,pid=1,value=vi,beg=0,size=16000")
    net.set_recorder("id=2,pid=1,value=vo,beg=0,size=16000")
    net.connect_syna()
    # First run
    net.set_params(0, "selid=0")
    net.set_params(1, "selid=0")
    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record1 = net.get_record(0)
    record2 = net.get_record(1)
    record3 = net.get_record(2)
    error1 = net.get_param(1, "error")
    # Second run
    net.set_params(0, "selid=1")
    net.set_params(1, "selid=1")
    net.reset()
    net.run(16000, 1.0 / 16000.0)
    record4 = net.get_record(0)
    record5 = net.get_record(1)
    record6 = net.get_record(2)
    error2 = net.get_param(1, "error")

    fig, ax = plt.subplots(2, 1, sharex='col')
    fig.suptitle('CellMultiData test')

    # plot 1
    ax[0].plot([i * 1.0 / 16000.0 for i in record1.pc], record1.data, '-',
               label="CellMultiData 100Hz")
    ax[0].plot([i * 1.0 / 16000.0 for i in record2.pc], record2.data, '-',
               label="Validator in 100Hz")
    ax[0].plot([i * 1.0 / 16000.0 for i in range(len(const1_arr))], const1_arr, '-',
               label="Validator data 100Hz")
    ax[0].plot([i * 1.0 / 16000.0 for i in record4.pc], record4.data, '-',
               label="CellMultiData 300Hz")
    ax[0].plot([i * 1.0 / 16000.0 for i in record5.pc], record5.data, '-',
               label="Validator in 300Hz")
    ax[0].plot([i * 1.0 / 16000.0 for i in range(len(const2_arr))], const2_arr, '-',
               label="Validator data 300Hz")
    ax[0].grid(True)
    ax[0].legend()

    # plot 2
    ax[1].plot([i * 1.0 / 16000.0 for i in range(len(const1_arr))],
               ((const1_arr-record2.data)*(const1_arr-record2.data)), '-',
               label="Calculated diff 100Hz")
    ax[1].plot([i * 1.0 / 16000.0 for i in record3.pc], record3.data, '.-',
               label="Validator out 100Hz")
    ax[1].plot([i * 1.0 / 16000.0 for i in range(len(const2_arr))],
               ((const2_arr - record5.data) * (const2_arr - record5.data)), '-',
               label="Calculated diff 300Hz")
    ax[1].plot([i * 1.0 / 16000.0 for i in record6.pc], record6.data, '.-',
               label="Validator out 300Hz")
    ax[1].grid(True)
    ax[1].legend()

    print(f"Net calculated error 1 is: {error1}")
    print(f"Data calculated error 1 is: "
          f"{sum(((const1_arr - record2.data) * (const1_arr - record2.data)))}")
    print(f"Net calculated error 2 is: {error2}")
    print(f"Net calculated error 2 is: "
          f"{sum(((const2_arr - record5.data) * (const2_arr - record5.data)))}")

    plt.xlabel("Time [s]")
    plt.show()

    return 0, "Success"


def plot_CellRLC_hf():

    api = synacell.cmodule.SnnAPI
    net = api.new_net()
    net.add_part("id=0,type=CellMultiData")

    # Create data
    amp = 10000
    size = 16000
    tmin = 0
    tmax = 1.0
    fstart = 0
    fstop = 250
    fstep = 1
    hf = np.zeros((2, int(round((fstop - fstart) / fstep + 0.5))), dtype=float)
    hf[0] = [freq for freq in range(fstart, fstop, fstep)]
    for i, freq in enumerate(hf[0]):
        func = signal.func_generator(func_name="sin", freq=freq, amp=amp, phase=0.5*math.pi)
        sig = signal.func_to_nparray(func=func, t_min=tmin, t_max=tmax, size=size, fixed_size=True)
        # Load data
        net.set_params_dbarr(0, f"fid={i},size={len(sig)}", sig)

    net.add_part("id=1000,type=SynaRCA,ciid=0,coid=1")
    net.add_part("id=1,type=CellRLC")
    net.add_part(f"id=3,type=CellEMA,alpha=0.001,sum=2")
    net.add_part(f"id=1003,type=SynaBuffer,ciid=1,coid=3")
    net.add_part(f"id=4,type=CellEMA,alpha=0.001,sum=1")
    net.add_part(f"id=3004,type=SynaBuffer,ciid=3,coid=4")

    net.connect_syna()

    for i, freq in enumerate(hf[0]):
        # Run net
        net.reset()
        net.set_params(0, f"selid={i}")
        net.run(size, 1.0 / 16000.0)

        # Calculate transfer function
        hf[1, i] = math.sqrt(2.0 * net.get_vo(4)) / amp

    # Run once more for printing
    # Set recorder
    net.set_recorder(f"id=0,pid=0,value=vo,beg=0,size={len(sig)}")
    net.set_recorder(f"id=1,pid=1,value=vi,beg=0,size={len(sig)}")
    net.set_recorder(f"id=2,pid=4,value=vo,beg=0,size={len(sig)}")
    net.reset()
    net.set_params(0, f"selid={160}")
    net.run(size, 1.0 / 16000.0)

    # Get data
    record = []
    record.append(net.get_record(0))
    record.append(net.get_record(1))
    record.append(net.get_record(2))

    print(f"vo = {net.get_vo(4)}, sig amplitude = {math.sqrt(2.0*net.get_vo(4))}")

    # Plot data
    fig, ax = plt.subplots(3, 1)
    fig.suptitle('Train CellRLC resonator')

    ax[0].plot([i * 1.0 / 16000.0 for i in record[0].pc], record[0].data, '-',
               label=f"Input signal")
    ax[0].grid(True)
    ax[0].legend()

    ax[1].plot([i * 1.0 / 16000.0 for i in record[0].pc], record[0].data, '-',
               label=f"Record 0")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[1].pc], record[1].data, '-',
               label=f"Record 1")
    ax[1].plot([i * 1.0 / 16000.0 for i in record[2].pc],
               [math.sqrt(2.0*val) for val in record[2].data], '-',
               label=f"Record 2")
    ax[1].grid(True)
    ax[1].legend()

    ax[2].plot(hf[0], hf[1], '-', label=f"H(f)")
    ax[2].grid(True)
    ax[2].legend()

    plt.show()


def run_part(part_name=""):
    if part_name == "CellEMA":
        plot_CellEMA()
        plot_CellEMA_sum()
    elif part_name == "CellMultiData":
        plot_CellMultiData()
        plot_CellMultiData_validate()
    elif part_name == "CellRLC":
        plot_CellRLC_hf()
    else:
        print(f"Part name '{part_name}' not recognized")


if __name__ == '__main__':
    '''
    1. If the module is ran (not imported) the interpreter sets this at the top of your module:
    ```
    __name__ = "__main__"
    ```
    2. If the module is imported: 
    ```
    import rk
    ```
    The interpreter sets this at the top of your module:
    ```
    __name__ = "rk"
    ```
    '''
    run_part("CellEMA")
    run_part("CellMultiData")
    run_part("CellRLC")