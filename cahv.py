"""Extract CAHV camera model from .LBL files"""

import re

MODEL_COMPONENT = ('C', 'A', 'H', 'V', 'O', 'R', 'E', 'P')
MODEL = dict()
PATH = 'D:\\Datasets\\labels\\0078ML0005760710102736E01_XXXX.LBL'


def main(path=PATH):
    """Extract CAHV* camera model from .LBL files

    :param path: `lbl` file's path
    :return: dict of camera model
    """

    with open(path, 'r') as file:
        txt = file.read()

        # For generating an iterator of raw camera model component information
        regex0 = re.compile(r'MODEL_COMPONENT_\d.*\n.*')
        model_component_iter = regex0.finditer(txt)

        # For extracting vector's component of each camera model component w.r.t. last iterator
        regex1 = re.compile(r'.*=\s\(\s(.*),\s(.*),\n(.*)\s.*')

        for idx, component in enumerate(model_component_iter):
            try:
                MODEL[MODEL_COMPONENT[idx]] = list()
                MODEL[MODEL_COMPONENT[idx]].append(float(regex1.sub(r'\1', component.group())))
                MODEL[MODEL_COMPONENT[idx]].append(float(regex1.sub(r'\2', component.group())))
                MODEL[MODEL_COMPONENT[idx]].append(float(regex1.sub(r'\3', component.group())))

            except ValueError:
                return None

            finally:
                continue
        return MODEL


if __name__ == "__main__":
    main()
