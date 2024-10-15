# FFmpeg Lightweight Simple Video Compressor

UI version for target folder and start convert all video files to hevc/h265 codec recursively

## Requirement

This project requires [FFmpeg](https://ffmpeg.org/download.html) to run, [FFmpeg](https://ffmpeg.org/download.html) must be accessible via `$PATH` environment variable.

## Instruction

1. Start the program by:
   - Run `python main.py`
   - Launch [ffmpeg-lightweight-video-compressor.exe](https://github.com/CGYCGY/ffmpeg-lightweight-video-compressor/releases/download/v1.0.0/ffmpeg-lightweight-video-compressor.exe)
2. Click `Load` and select the folder of your videos located at
3. Choose what happen if files already exist, options available: [[3]](#note)
   - Ask everytime
   - Overwrite files if exist
   - Skip files if exist
   - Delete files if exist
4. Click `Compress!` to start compress your videos
5. Ways to force stop:
   - Navigate to the console window, press `ctrl+c`

### Note
1. All videos will be converted to `.mp4`
2. If the video format is `.mp4`, it will be renamed before the conversion started to avoid filename conflict
3. If the video format is not `.mp4` and there is another same filename video exist with `.mp4` extension, file exist options will be take into consideration
   ```
   Example:

   --abc.ts
   --abc.mp4

   preparing to convert abc.ts to abc.mp4 with hevc codec...
   ops! file already exist, what to do?
   check file exist option selected by user!
   ```
4. Supported video format: `.ts`, `.mp4`, `.mov`, `.mkv`, `.avi`, `.wmv`, `.webm`, `.flv`
5. Tested video format: `.ts`, `.mp4`

### Extras
1. Generate executable file by:
   - Run `pyinstaller --onefile .\main.py --name=ffmpeg-lightweight-video-compressor`