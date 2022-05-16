import os
import sys


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
    return o


def convert_to_mp4(bd, r, fn, o):
    ori = os.path.join(bd, r[2:], fn)
    if not ori.lower().endswith('.mp4'):
        mp4 = os.path.splitext(ori)[0] + '.mp4'
        o = check_exist(mp4, o)
        if o:
            print('convert', ori, 'to', mp4, sep='\n')
            os.system('ffmpeg {overwrite} -i "{source}" -c copy "{output}"'.format(source=ori, output=mp4, overwrite=o))


def compress(bd, r, fn, o):
    ori = os.path.join(bd, r[2:], fn)
    codec = os.popen('ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of '
                     'default=noprint_wrappers=1:nokey=1 "{0}"'.format(ori)).read()
    # check codec
    if codec.strip() != 'hevc':
        pos = len(ori) - 4
        temp = ori[:pos] + '_' + ori[pos:]
        hevc = os.path.splitext(ori)[0] + '.mp4'

        o = check_exist(hevc, o)
        if o:
            print('Start compress', ori, sep='\n')
            os.rename(ori, temp)
            os.system('ffmpeg {overwrite} -i "{source}" -vcodec libx265 -crf 30 "{output}"'
                      .format(source=temp, output=hevc, overwrite=o))
            os.remove(temp)
            print('Compressed')


def main(basedir=os.getcwd(), overwrite=''):
    print('Selected Folder', '===============', basedir, '===============', sep='\n')
    # loop files
    for root, dirs, files in os.walk(basedir):
        for filename in files:
            if os.path.splitext(filename)[1] in ['.ts', '.mp4', 'mov', '.mkv', '.avi', '.wmv', '.webm', '.flv']:
                compress(basedir, root, filename, overwrite)

    print('Completed')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
