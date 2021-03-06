import os
import sys
import ffmpeg
from videoprops import get_video_properties

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


def convert_to_mp4(bd, r, fn, o):
    ori = os.path.join(bd, r[2:], fn)
    if not ori.lower().endswith('.mp4'):
        mp4 = os.path.splitext(ori)[0] + '.mp4'
        o = check_exist(mp4, o)
        if o:
            print('convert', ori, 'to', mp4, sep='\n')
            try:
                # ffmpeg -i "fullname" -c copy "mp4name"
                ffmpeg.input(ori).output(mp4, c='copy').global_args(o).run()
            except Exception as exp:
                print()


def compress(bd, r, fn, o):
    global compress_count
    ori = os.path.join(bd, r[2:], fn)
    props = get_video_properties(ori)

    # check codec
    if props['codec_name'] != 'hevc':
        pos = len(ori) - 4
        temp = ori[:pos] + '_' + ori[pos:]
        hevc = os.path.splitext(ori)[0] + '.mp4'

        o = check_exist(hevc, o)
        if o:
            print('Start compress', ori, sep='\n')
            try:
                os.rename(ori, temp)
                # ffmpeg -i "temp" -vcodec libx265 -crf 30 "hevc"
                ffmpeg.input(temp).output(hevc, vcodec='libx265', crf=30).global_args(o).run(overwrite_output=True)
                os.remove(temp)
                compress_count += 1
                print('Compressed')
            except Exception as exp:
                print()


def main(basedir=os.getcwd(), overwrite=''):
    print('Selected Folder', '===============', basedir, '===============', sep='\n')
    # loop files
    count = 0
    for root, dirs, files in os.walk(basedir):
        for filename in files:
            if os.path.splitext(filename)[1] in ['.ts', '.mp4', 'mov', '.mkv', '.avi', '.wmv', '.webm', '.flv']:
                count += 1
                print('Count: ', count)
                compress(basedir, root, filename, overwrite)

    print('Total video scanned:', count)
    print('Total video compressed:', compress_count)
    print('Completed')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
