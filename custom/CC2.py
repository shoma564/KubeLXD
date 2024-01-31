from kubernetes import client, config
import time

class CustomController:
    def __init__(self):
        config.load_kube_config()
        self.api = client.CustomObjectsApi()

    def fetch_tasks_from_crd(self):
        group = 'example.com'
        version = 'v1'
        plural = 'tasks'
        namespace = 'default'

        try:
            cr_list = self.api.list_namespaced_custom_object(group, version, namespace, plural)
            tasks = []

            for cr in cr_list['items']:
                task = {
                    'action': cr['spec'].get('action', ''),
                    'container_name': cr['spec'].get('containerName', ''),
                    # Add other necessary information based on your CRD
                }
                tasks.append(task)

            return tasks

        except Exception as e:
            print("Exception when calling CustomObjectsApi->list_namespaced_custom_object: %s\n" % e)

    def execute_task(self, task):
        action = task['action']
        container_name = task['container_name']

        if action == 'create_container':
            # Call function to create container with given name
            self.create_container(container_name)
        elif action == 'start_container':
            # Call function to start container with given name
            self.start_container(container_name)
        elif action == 'stop_container':
            # Call function to stop container with given name
            self.stop_container(container_name)
        elif action == 'delete_container':
            # Call function to delete container with given name
            self.delete_container(container_name)
        else:
            print("Unknown action:", action)

    def create_container(self, container_name):
        # Implement function to create container
        print("Creating container:", container_name)

    def start_container(self, container_name):
        # Implement function to start container
        print("Starting container:", container_name)

    def stop_container(self, container_name):
        # Implement function to stop container
        print("Stopping container:", container_name)

    def delete_container(self, container_name):
        # Implement function to delete container
        print("Deleting container:", container_name)

if __name__ == "__main__":
    controller = CustomController()

    while True:
        tasks = controller.fetch_tasks_from_crd()
        if tasks:
            print("Received tasks:", tasks)
            for task in tasks:
                controller.execute_task(task)
        else:
            print("No tasks received.")
        time.sleep(5)  # Poll CRD every 5 seconds for new tasks
