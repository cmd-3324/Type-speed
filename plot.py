

import matplotlib.pyplot as plt

def plot_scores(scores):
    rounds = list(range(1, len(scores) + 1))
    wpms = [s["wpm"] for s in scores]
    
    plt.figure(figsize=(8, 4))
    plt.plot(rounds, wpms, marker="o", color="cyan", linewidth=2) #scatter - barch - bar - hist 
    plt.xlabel("Round")
    plt.ylabel("Words Per Minute (WPM)")
    plt.title("Typing Speed Progress")
    plt.grid(True, alpha=0.3)
    plt.savefig("speed_test.png")
    plt.close()