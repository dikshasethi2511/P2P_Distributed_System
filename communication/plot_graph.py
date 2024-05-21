import matplotlib.pyplot as plt
import pandas as pd


def plot_metrics(file_path):
    data = pd.read_csv(file_path)

    # Plot CPU utilization
    plt.figure(figsize=(10, 6))
    plt.plot(data["timestamp"], data["cpu_percent"], label="CPU Utilization (%)")
    plt.xlabel("Timestamp")
    plt.ylabel("CPU Utilization (%)")
    plt.title("CPU Utilization Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig("cpu_utilization.png")  # Save the plot as a file
    plt.close()

    # Plot RAM utilization
    plt.figure(figsize=(10, 6))
    plt.plot(data["timestamp"], data["ram_percent"], label="RAM Utilization (%)")
    plt.xlabel("Timestamp")
    plt.ylabel("RAM Utilization (%)")
    plt.title("RAM Utilization Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig("ram_utilization.png")  # Save the plot as a file
    plt.close()

    # Plot Storage utilization
    plt.figure(figsize=(10, 6))
    plt.plot(data["timestamp"], data["storage_used"], label="Storage Used (bytes)")
    plt.xlabel("Timestamp")
    plt.ylabel("Storage Used (bytes)")
    plt.title("Storage Utilization Over Time")
    plt.legend()
    plt.grid(True)
    plt.savefig("storage_utilization.png")  # Save the plot as a file
    plt.close()


# Call the plotting function
plot_metrics("metrics.txt")
