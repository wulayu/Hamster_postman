import PIL.Image
import os
import time

from carvekit.api.interface import Interface
from carvekit.ml.wrap.fba_matting import FBAMatting
from carvekit.ml.wrap.u2net import U2NET
from carvekit.pipelines.postprocessing import MattingMethod
from carvekit.pipelines.preprocessing import PreprocessingStub
from carvekit.trimap.generator import TrimapGenerator

source = "../../source/"
out_path = "../../output/image-background-remove-tool/"
if not os.path.isdir(out_path):
    os.mkdir(out_path)

time_start = time.time()

for index, file_name in enumerate(os.listdir(source)):
    if file_name != '02-927.jpg':
        continue
    input_path = file_name
    output_path = 'output_' + str(index) + '.png'

    u2net = U2NET(device='cpu', batch_size=1)
    fba = FBAMatting(device='cpu', input_tensor_size=2048, batch_size=1)
    trimap = TrimapGenerator()
    preprocessing = PreprocessingStub()
    postprocessing = MattingMethod(matting_module=fba, trimap_generator=trimap, device='cpu')
    interface = Interface(pre_pipe=preprocessing, post_pipe=postprocessing, seg_pipe=u2net)

    image = PIL.Image.open(os.path.join(source, input_path))
    image = image.convert(mode='RGBA')
    cat_wo_bg = interface([image])[0]
    cat_wo_bg.save(os.path.join(out_path, output_path), format='png')

    print(str(index + 1) + '/' + str(len(os.listdir(source))) + '\n')

time_end = time.time()
print('time cost', time_end - time_start, 's')
