import pandas as pd
from google.cloud import translate_v2 as translate
import six

df = pd.read_csv('static/dashboard/all.csv')
for x in range(0, 1918106):
    df.head(1)
    if x % 10 == 0:
        print(x)

    translate_client = translate.Client()
    translations = {}
    for column in df.columns:
        # Unique elements of the column
        unique_elements = df[column].unique()
        for element in unique_elements:
            if str(element[0].isspace()):
                element = element[:-1]

                if str(element[0]) == "'":

                    print(True)
                    str(element).replace("'", "")
            print(element)
            if isinstance(element, six.binary_type):
                element = element.decode("utf-8")
            # Adding all the translations to a dictionary (translations)
            translations[element] = translate_client.translate(element, target_language="en")
    print(translations)

    df.replace(translations, inplace=True)
    df.head(1)