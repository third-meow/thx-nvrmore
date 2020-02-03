
# Orginal format:
# nvrmore - [album] - [song no.] [name][(feat.)].wav
# Desired format:
# [album]-[name].wav
#
# Notes:
#   - Album, name and feat may contain spaces

import os

def main():
    
    # for all files in songs directory
    for filename in os.listdir('songs/'):
        if filename.endswith('.wav'):
            # get album and title with track number from filename
            _, album, title_and_number = filename.split('-', 2)

            # remove spaces from album
            stripped_album = album.strip()
            stripped_album_no_spaces = stripped_album.replace(' ', '_')

            # remove track number and spaces from title
            title = title_and_number.split(' ', 2)[2]
            stripped_title = title.split('.')[0].split('(')[0].strip()
            stripped_title_no_spaces = stripped_title.replace(' ', '_')

            # rebuild filename in new format
            new_format = []
            new_format.append(stripped_album_no_spaces)
            new_format.append('-')
            new_format.append(stripped_title_no_spaces)
            new_format.append('.wav')

            new_filename = ''.join(new_format)

            # rename file
            os.rename('songs/'+filename, 'songs/'+new_filename)


if __name__ == '__main__':
    main()
