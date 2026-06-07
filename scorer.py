
def calculate_score(target, user_input, elapsed_seconds):
    """Return WPM and accuracy %."""
    
    # Accuracy: how many characters matched
    correct = sum(1 for t, u in zip(target, user_input) if t == u)
    total = len(target)
    accuracy = (correct / total) * 100 if total > 0 else 0
    
    # WPM = (characters typed / 5) / minutes
    # 5 characters = 1 "word" in typing tests
    minutes = elapsed_seconds / 60
    wpm = (len(user_input) / 5) / minutes if minutes > 0 else 0
    
    return round(wpm, 1), round(accuracy, 1)