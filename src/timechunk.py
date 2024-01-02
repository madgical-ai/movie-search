
def create_chunks(filename):  # 300 seconds = 5 minutes
    target_time_interval=600
    # Open and read the content of the file
    with open(filename, 'r') as file:
        content = file.read()

    # Regular expression to match the subtitle blocks in VTT format
    pattern = re.compile(r'(\d+)\n(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.+?)(?=\n\d+|$)', re.DOTALL)

    matches = pattern.findall(content)

    weaviateData = []
    current_chunk = ""
    current_start_time = []
    current_start_time_seconds = None
    current_end_time = None
    current_end_time_seconds = None
    totalDuration = None  # You need to set the total video duration
    final_end_Time = None

    for match in matches:
        index, start_time, end_time, text = match

        final_end_Time = end_time

        # Convert start and end time to seconds including milliseconds
        start_time_components = start_time.split(':')
        start_time_seconds = (
            int(start_time_components[0]) * 3600 +  # hours to seconds
            int(start_time_components[1]) * 60 +    # minutes to seconds
            float(start_time_components[2])         # seconds including milliseconds
        )

        end_time_components = end_time.split(':')
        end_time_seconds = (
            int(end_time_components[0]) * 3600 +  # hours to seconds
            int(end_time_components[1]) * 60 +    # minutes to seconds
            float(end_time_components[2])         # seconds including milliseconds
        )

        if current_start_time_seconds is None:
            current_start_time_seconds = start_time_seconds
            current_start_time.append(start_time)

        # Check if adding the current text will exceed the target time interval
        if end_time_seconds - current_start_time_seconds <= target_time_interval:
            # Add to the current chunk
            current_chunk += text.strip() + ' '
            current_end_time = end_time
            current_end_time_seconds = end_time_seconds
        else:
            # Save the current chunk and start a new one
            weaviateData.append({
                'start_time': current_start_time[0],
                'end_time': current_end_time,
                'start_time_seconds': current_start_time_seconds,
                'end_time_seconds': current_end_time_seconds,
                'text': current_chunk.strip(),
            })

            # Reset for the new chunk
            current_chunk = text.strip() + ' '
            current_start_time_seconds = start_time_seconds
            current_end_time_seconds = end_time_seconds
            current_start_time.clear()
            current_start_time.append(start_time)

            print(f"start_time: -----------{current_start_time}---")
            print(f"end_time: -------sec                               ----{current_end_time_seconds}---")
            print(f"end_time: -----------{current_end_time}---")
            print(f"end_time: -------                         @@@@@----{end_time}---")

    # Save the last chunk if it exists
    print("--------------------appending this chunk------------------------")
    if current_chunk:
        weaviateData.append({
            'start_time': current_start_time[0],
            'end_time': final_end_Time,
            'start_time_seconds': current_start_time_seconds,
            'end_time_seconds': current_end_time_seconds,
            'text': current_chunk.strip(),
        })
        print({
            'start_time': current_start_time[0],
            'end_time': final_end_Time,
            'start_time_seconds': current_start_time_seconds,
            'end_time_seconds': current_end_time_seconds,
            'text': current_chunk.strip(),
        })
    print("--------------------appending this chunk------------------------")

    return weaviateData