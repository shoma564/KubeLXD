import time
import pylxd

class LXDController:
    def __init__(self, lxd_host):
        self.client = pylxd.Client(endpoint='https://' + lxd_host, verify=False)

    def create_container(self, container_name, image, network=None, cpu=None, memory=None):
        config = {'name': container_name, 'source': {'type': 'image', 'alias': image}}
        if network:
            config['devices'] = {'eth0': {'nictype': 'bridged', 'parent': network, 'type': 'nic'}}
        if cpu:
            config['devices']['cpu'] = {'limits': {'cpu': cpu}}
        if memory:
            config['devices']['memory'] = {'limits': memory}

        container = self.client.containers.create(config, wait=True)
        return container

    def start_container(self, container_name):
        container = self.client.containers.get(container_name)
        container.start(wait=True)

    def stop_container(self, container_name):
        container = self.client.containers.get(container_name)
        container.stop(wait=True)

    def delete_container(self, container_name):
        container = self.client.containers.get(container_name)
        container.delete(wait=True)


if __name__ == "__main__":
    lxd_host = '172.24.20.100'
    lxd_controller = LXDController(lxd_host)


    while True:
        # メインロジックの処理
        print("Main loop: Checking for new tasks...")

        # 例: タスクのリストを取得して、それに基づいてコンテナを作成する
        tasks = fetch_tasks_from_somewhere()  # タスクの取得方法はアプリケーションに依存します

        for task in tasks:
            if task['action'] == 'create_container':
                lxd_controller.create_container(task['container_name'], task['image'], task.get('network'), task.get('cpu'), task.get('memory'))
            elif task['action'] == 'start_container':
                lxd_controller.start_container(task['container_name'])
            elif task['action'] == 'stop_container':
                lxd_controller.stop_container(task['container_name'])
            elif task['action'] == 'delete_container':
                lxd_controller.delete_container(task['container_name'])
            else:
                print(f"Unknown action: {task['action']}")

        time.sleep(5)  # 例えば5秒ごとにループを実行する
