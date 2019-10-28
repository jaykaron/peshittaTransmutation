import os
import re

"""
A script for converting the peshitta translation of the old testament from its original
syriac script to the modern hebrew script.
Takes the raw files downloaded from http://cal.huc.edu/ in the directory 'raw/' and spits
them out to the 'converted/' directory.
"""

def multireplace(string, replacements):
    """
    Given a string and a replacement map, it returns the replaced string.
    :param str string: string to execute replacements on
    :param dict replacements: replacement dictionary {value to find: value to replace}
    :rtype: str
    """
    # Place longer ones first to keep shorter substrings from matching where the longer ones should take place
    # For instance given the replacements {'ab': 'AB', 'abc': 'ABC'} against the string 'hey abc', it should produce
    # 'hey ABC' and not 'hey ABc'
    substrs = sorted(replacements, key=len, reverse=True)

    # Create a big OR regex that matches any of the substrings to replace
    regexp = re.compile('|'.join(map(re.escape, substrs)))

    # For each match, look up the new string in the replacements
    return regexp.sub(lambda match: replacements[match.group(0)], string)


hebrew = range(1488, 1514 + 1)

# maps syriac letters to hebrew
alphabet_map = {
    '\N{Syriac Letter Alaph}': '\N{Hebrew Letter Alef}',       #  aleph
    '\N{Syriac Letter Beth}': '\N{Hebrew Letter Bet}',
    '\N{Syriac Letter Gamal}': '\N{Hebrew Letter Gimel}',
    '\N{Syriac Letter Dalath}': '\N{Hebrew Letter Dalet}',
    '\N{Syriac Letter He}': '\N{Hebrew Letter He}',
    '\N{Syriac Letter Waw}': '\N{Hebrew Letter Vav}',
    '\N{Syriac Letter Zain}': '\N{Hebrew Letter Zayin}',
    '\N{Syriac Letter Heth}': '\N{Hebrew Letter Het}',
    '\N{Syriac Letter Teth}': '\N{Hebrew Letter Tet}',
    '\N{Syriac Letter Yudh}': '\N{Hebrew Letter Yod}',       # yud
    '\N{Syriac Letter Kaph}': '\N{Hebrew Letter Kaf}',
    '\N{Syriac Letter Lamadh}': '\N{Hebrew Letter Lamed}',
    '\N{Syriac Letter Mim}': '\N{Hebrew Letter Mem}',
    '\N{Syriac Letter Nun}': '\N{Hebrew Letter Nun}',
    '\N{Syriac Letter Semkath}': '\N{Hebrew Letter Samekh}',
    '\N{Syriac Letter E}': '\N{Hebrew Letter Ayin}',
    '\N{Syriac Letter Pe}': '\N{Hebrew Letter Pe}',
    '\N{Syriac Letter Sadhe}': '\N{Hebrew Letter Tsadi}',
    '\N{Syriac Letter Qaph}': '\N{Hebrew Letter Qof}',
    '\N{Syriac Letter Rish}': '\N{Hebrew Letter Resh}',
    '\N{Syriac Letter Shin}': '\N{Hebrew Letter Shin}',
    '\N{Syriac Letter Taw}': '\N{Hebrew Letter Tav}'
}

replacement_map_1 = {
    '\N{Hebrew Letter He}' + '\N{Syriac Rwaha}': '\N{Hebrew Letter He}' + '\N{Hebrew Mark Upper Dot}',		#mapik he
    '\N{Syriac Sublinear Full Stop}  ': '\N{Full Stop}  ',
    '\N{Syriac End of Paragraph}  ': '\N{Full Stop}  '

}

# characters to delete by replacing with empty string
deletables = [
    '\N{Syriac End of Paragraph}',      # diamond
    '\N{Syriac Supralinear Colon}',
    '\N{Syriac Hbasa-Esasa Dotted}',
    '\N{Syriac Sublinear Full Stop}',
    '\N{Syriac Rwaha}'
    ]

sofit_letters = {
    '\N{Hebrew Letter Kaf}': '\N{Hebrew Letter Final Kaf}',
    '\N{Hebrew Letter Mem}': '\N{Hebrew Letter Final Mem}',
    '\N{Hebrew Letter Nun}': '\N{Hebrew Letter Final Nun}',
    '\N{Hebrew Letter Pe}': '\N{Hebrew Letter Final Pe}',
    '\N{Hebrew Letter Tsadi}': '\N{Hebrew Letter Final Tsadi}'
}

def flip_numbers(matchobj):
    """
    Reverses the first match in the group
    """
    return matchobj.group(0)[::-1]

def end_letters(matchobj):
    original = matchobj.group(1)
    sofit = sofit_letters[original]
    return matchobj.group(0).replace(original, sofit)

book_names = ["1Ch", "1K", "1S", "2Ch", "2K", "2S", "Am", "Daniel", "Dt", "Eccl", "Esth", "Ex", "Ez", "Ezra", "Gn", "Hab",
    "Hag", "Ho", "Is", "Je", "Job", "Joel", "Jonah", "Jos", "Ju", "Lam", "Lv", "Ma", "Mi", "Na", "Neh", "Nm", "Ob", "Prov",
    "Ps", "Ruth", "Song", "Ze", "Zep"]

for book in book_names:
    in_file_path = os.path.join("raw", book + ".txt")
    out_file_path = os.path.join("converted", book + ".txt")

    with open(in_file_path, "r") as in_file:
        with open(out_file_path, "w") as out_file:
            for l in in_file:
                alpha_swap = multireplace(l, alphabet_map)      # swap languages
                rep1 = multireplace(alpha_swap, replacement_map_1)  # non single letter swaps
                delete_some = multireplace(rep1, {e:"" for e in deletables})    # remove all from 'deletables'
                flipped = re.sub(r'\d+:\d+', flip_numbers, delete_some)         # reverses the verse numbers


                # syriac doesn't have sofit letters, so the letters that should be sofits
                # in hebrew need to be found and replaced

                all_sofits = '|'.join(sofit_letters.keys())

                # any sofit followed by an optional colon, space or punctuation
                reg = r'({sofits})({colon}?[ .#/])'.format(sofits=all_sofits, colon='\N{Combining Diaeresis}')
                final = re.sub(reg, end_letters, flipped)

                print(final, file=out_file)
