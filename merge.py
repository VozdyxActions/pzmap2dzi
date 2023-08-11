import os
import yaml
import datetime

from PIL import Image
from pzmap2dzi.mptask import Task, SplitScheduler


class MergeHeightWorker(object):
    def on_job(self, job):
        print(f'Job: {job[0]}')
        file_number, layer, layer0 = job
        # if file_number != 100:
        #     return
        print('Start merge...')

        start = datetime.datetime.utcnow()
        tmp = []

        for file in layer0.get(file_number):
            img = Image.open(file)
            tmp.append(img)

        h = 0
        w = 0

        for image in tmp:
            h += image.height
            w = image.width

        dst = Image.new('RGB', (w, h))
        h = 0

        for image in tmp:
            dst.paste(image, (0, h))
            h += image.height

        if file_number == 100:
            dst.show()
            dst.save(f'E:\\out\\{file_number}.png', 'png')
            print('End merge at {}'.format(datetime.datetime.utcnow() - start))



# def init(self):
#     return True

# def on_msg(self, msg):
#     print(f'Msg: {msg}')


with open('conf.yaml', 'r') as f:
    conf = yaml.safe_load(f.read())

d = '\\'
input_path = conf['output_path'] + r'\html\base'


def main():
    files = {}

    for filename in os.listdir(input_path):
        if filename.startswith('layer') and os.path.isdir(path := input_path + d + filename):
            layer = {}
            for file in os.listdir(path := path + d + '18'):
                x, y = file[:-4].split('_')
                if not layer.get(int(x)):
                    layer[int(x)] = []
                layer[int(x)].append(path + d + file)
            files.update({filename[:6]: layer})

    print('----------------------------------------------')
    return files


def run_merge(files):
    layer0: dict = files['layer0']
    layer: list = list(files['layer0'].keys())
    layer.sort()

    img_x = {}

    for file_number in layer:
        if file_number != 100:
            continue
        print('Start merge...')

        start = datetime.datetime.utcnow()
        tmp = []

        for file in layer0.get(file_number):
            img = Image.open(file)
            tmp.append(img)

        h = 0
        w = 0

        for image in tmp:
            h += image.height
            w = image.width

        dst = Image.new('RGB', (w, h))
        h = 0

        for image in tmp:
            dst.paste(image, (0, h))
            h += image.height

        if file_number == 100:
            dst.show()
            print('End merge at {}'.format(datetime.datetime.utcnow() - start))

    print('End script at {}'.format(datetime.datetime.utcnow() - start_script))
    exit()


def test():
    files = main()
    layer0: dict = files['layer0']
    layer: list = list(files['layer0'].keys())
    layer.sort()

    tasks = []
    for i in layer:
        tasks.append([i, layer0.get(i), layer0])

    worker = MergeHeightWorker()
    task = Task(worker, SplitScheduler(True))
    task.run(tasks, 6)


if __name__ == '__main__':
    start_script = datetime.datetime.utcnow()
    test()
    print('End script at {}'.format(datetime.datetime.utcnow() - start_script))
