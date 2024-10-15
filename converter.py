import os
import re
import sys

compress_count = 0


def check_exist(hevc, o):
    # check converted filename existence
    if os.path.exists(hevc):
        print(hevc)
        if o == '':
            while True:
                ov = input('File exist, overwrite file? (y/n)')
                if ov.lower() == 'n':
                    return False
                elif ov.lower() == 'y':
                    return '-y'
                else:
                    print('Invalid input')
        elif not o:
            print('File exist, skipped')
            return False
    elif o != '' and not o:  # o == False
        return ''
    return o


def convert_to_mp4(bd, r, fn, o, rm):
    ori = os.path.join(bd, r[2:], fn)
    if not ori.lower().endswith('.mp4'):
        mp4 = os.path.splitext(ori)[0] + '.mp4'
        o = check_exist(mp4, o)
        if o:
            print('convert', ori, 'to', mp4, sep='\n')
            if re.match('^[a-zA-Z]{2,5}-\d{3,4}', ori):
                os.system('ffmpeg {overwrite} -i "{source}" -c copy "{output}"'.format(source=ori, output=mp4, overwrite=o))
                if rm:
                    os.remove(ori)
            else:
                os.system('ffmpeg {overwrite} -i "{source}" -c:v copy "{output}"'.format(source=ori, output=mp4, overwrite=o))
                if rm:
                    os.remove(ori)


def compress(bd, r, fn, o):
    global compress_count
    ori = os.path.join(bd, r[2:], fn)
    codec = os.popen('ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of '
                     'default=noprint_wrappers=1:nokey=1 "{0}"'.format(ori)).read()
    # check codec
    if codec.strip() != 'hevc':
        pos = len(ori) - 4
        temp = ori[:pos] + '_' + ori[pos:]
        hevc = os.path.splitext(ori)[0] + '.mp4'

        o = check_exist(hevc, o)
        if isinstance(o, str):
            print('Start compress', ori, sep='\n')
            os.rename(ori, temp)
            os.system('ffmpeg {overwrite} -hwaccel cuda -hwaccel_output_format cuda -i "{source}" -c:v hevc_nvenc -preset p7 -cq 32 -c:a copy "{output}"'
                      .format(source=temp, output=hevc, overwrite=o))
            os.remove(temp)
            compress_count += 1
            print('Compressed')


def main(mode='compress', basedir=os.getcwd(), overwrite='', remove=True):
    global compress_count
    print('Selected Folder', '===============', basedir, '===============', sep='\n')
    # loop files
    count = 0
    for root, dirs, files in os.walk(basedir):
        for filename in files:
            if os.path.splitext(filename)[1] in ['.ts', '.mp4', 'mov', '.mkv', '.avi', '.wmv', '.webm', '.flv']:
                count += 1
                print('Count: ', count)
                if mode == 'compress':
                    compress(basedir, root, filename, overwrite)
                elif mode == 'convert_to_mp4':
                    convert_to_mp4(basedir, root, filename, overwrite, remove)

    print('Total video scanned:', count)
    print('Total video compressed:', compress_count)
    print('Completed')
    compress_count = 0


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
