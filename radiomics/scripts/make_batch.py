import argparse
import csv
import logging
import os
from tifffile import imread
import SimpleITK as sitk
def read_and_write(fname):
  img = imread(fname)
  img = img.astype('float32')
  img_itk = sitk.GetImageFromArray(img)
  sitk.WriteImage(img_itk, fname)

class MakeCases(object):
  def __init__(self, custom_arguments=None):
    self.logger = logging.getLogger('radiomics.script')  # holds logger for script events
    self.relative_path_start = os.getcwd()
    self.args = self.getParser().parse_args(args=custom_arguments)  # Exits with code 2 if parsing fails

  def run(self):
    input_path, mask_path, output_file_path = self.args.images, self.args.labels, self.args.output
    if len(os.path.dirname(output_file_path)) == 0:
      output_path = os.getcwd()
      output_file_path = os.path.join(output_path, output_file_path)

    headers = ['ID', 'Image', 'Mask']
    input_names = sorted(os.listdir(input_path))
    mask_names = sorted(os.listdir(mask_path))
    print('output_file_path: ', output_file_path)
    with open(output_file_path, 'w') as output_file:
      writer = csv.writer(output_file, lineterminator='\n')
      writer.writerow(headers)
      for input_name, mask_name in zip(input_names, mask_names):
        name = input_name.split('.')[0]
        row = [name, os.path.join(input_path,input_name),  os.path.join(mask_path, mask_name)]
        if mask_name.endswith('tif') or mask_name.endswith('tiff'):
          read_and_write(row[2])
        writer.writerow(row)
  @classmethod
  def getParser(self):
    parser = argparse.ArgumentParser()

    parser.add_argument('images',
                        help='Path to the raw images}',
                        type=str)

    parser.add_argument('labels',
                        help='Path to the labeled images.',
                        type=str)
    parser.add_argument('output',
                        help='Path to the cases csv',
                        type=str)
    return parser


def parse_args():
  try:
    return MakeCases().run()
  except Exception as e:
    logging.getLogger().error("Error executing MakeCases command line!", exc_info=True)
    print("Error executing MakeCases command line!\n%s" % e)
    return 4
