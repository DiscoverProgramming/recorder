from lib import lib

delay = float(input("Delay between screenshots(Seconds): "))
start_index = int(input("Starting index for image names: "))
interval = float(input("Interval between frames shown on video(Seconds): "))


capture = lib(delay=delay, start_index=start_index, dir="imgs/", interval=interval)

capture.run()
