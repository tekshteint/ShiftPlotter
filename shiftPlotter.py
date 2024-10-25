import matplotlib.pyplot as plt
import numpy as np
import argparse
import pickle

def getGearRatios():
    gearRatios = []
    numOfGears = int(input("Enter the number of gears: "))
    
    for gear in range(numOfGears):
        print(f"Enter the gear ratio for gear {gear + 1}: ")
        gearRatios.append(float(input()))
        
    finalDrive = float(input("Enter the final drive ratio: "))
    gearRatios.append(finalDrive)
    
    print("Is this correct?")
    for gear in range(numOfGears):
        print(f"Gear {gear + 1}: {gearRatios[gear]}")
        
    print(f"Final Drive: {gearRatios[-1]}")
    
    correct = input("Y/N: ")
    if correct.lower() == "y":
        return gearRatios
    else:
        newRatios = getGearRatios()  
        return newRatios
    
def getRedline():
    redline = float(input("Enter the redline RPM: "))
    return redline

def getTireSize():
    tireSize = float(input("Enter the tire size in inches: "))
    return tireSize

def plotShiftPoints(gearRatios, redline, tireSize, save_path=None):
    finalDrive = gearRatios[-1]
    shiftSpeeds = []
    
    for gear in range(len(gearRatios) - 1):
        currentGearRatio = gearRatios[gear]
        maxSpeedInGear = (redline * tireSize * np.pi) / (finalDrive * currentGearRatio * 1056)
        
        speeds = np.linspace(shiftSpeeds[-1] if shiftSpeeds else 0, maxSpeedInGear, 100)
        rpms = (speeds * finalDrive * currentGearRatio * 1056) / (tireSize * np.pi)
        
        plt.plot(speeds, rpms, label=f'Gear {gear + 1}')
        
        if gear < len(gearRatios) - 2:
            nextGearRatio = gearRatios[gear + 1]
        
        shiftSpeeds.append(maxSpeedInGear)

    plt.xlabel('Wheel Speed (MPH)')
    plt.ylabel('Engine RPM')
    plt.title('Wheel Speed vs RPM for Different Gear Ratios')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(loc='upper right')
    plt.xlim(0, shiftSpeeds[-1] + 10)  
    plt.ylim(0, redline + 1000)  
    
    if save_path:
        with open(save_path, 'wb') as f:
            pickle.dump(plt.gcf(), f)
        print(f"Plot saved to {save_path}")
    else:
        plt.show()

def openAndPlotGML(file_path):
    with open(file_path, 'rb') as f:
        fig = pickle.load(f)
    fig.show()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="Shift Plotter")
    parser.add_argument('--save', type=str, help="Path to save the plot as a .gml file")
    parser.add_argument('--open', type=str, help="Path to open an existing .gml file")
    args = parser.parse_args()

    if args.open:
        openAndPlotGML(args.open)
    else:
        gearRatios = getGearRatios()
        redline = getRedline()
        tireSize = getTireSize()
        plotShiftPoints(gearRatios, redline, tireSize, save_path=args.save)

if __name__ == "__main__":
    main()