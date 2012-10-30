from datetime import timedelta

# This table resolves duration indices to actual time deltas for
# determining if a birthday needs a reminder.

durations = [timedelta(days=1),
             timedelta(days=3),
             timedelta(days=7),
             timedelta(days=14),
             timedelta(days=30)]