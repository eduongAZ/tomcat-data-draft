from datetime import datetime, timezone

import numpy as np


def iso_from_unix_time(unix_timestamps):
    # Function to convert a single timestamp
    def _convert_timestamp(unix_timestamp):
        utc_time = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc).isoformat()
        return utc_time.replace('+00:00', 'Z')

    # Vectorize the function
    vfunc = np.vectorize(_convert_timestamp)

    # Apply it to all timestamps
    iso_times = vfunc(unix_timestamps)

    return iso_times
