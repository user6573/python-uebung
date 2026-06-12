import unittest
import flask_todo
from flask_todo import app

class TestFlaskTodo(unittest.TestCase):

    def setUp(self):
        # test client von flask
        self.client = app.test_client()
        # liste vor jedem test leeren weil sie global ist
        flask_todo.tasks.clear()
        flask_todo.task_id_counter = 1

    def test_task_hinzufuegen(self):
        resp = self.client.post('/tasks', json={"title": "Hausuebung machen"})
        self.assertEqual(resp.status_code, 201)
        data = resp.get_json()
        self.assertEqual(data['title'], "Hausuebung machen")
        self.assertEqual(data['done'], False)
        self.assertEqual(data['id'], 1)

    def test_task_ohne_titel(self):
        resp = self.client.post('/tasks', json={"title": ""})
        self.assertEqual(resp.status_code, 400)

    def test_alle_tasks(self):
        self.client.post('/tasks', json={"title": "Task 1"})
        self.client.post('/tasks', json={"title": "Task 2"})
        resp = self.client.get('/tasks')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.get_json()), 2)

    def test_einzelner_task(self):
        self.client.post('/tasks', json={"title": "Test"})
        resp = self.client.get('/tasks/1')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()['title'], "Test")

    def test_task_nicht_gefunden(self):
        resp = self.client.get('/tasks/99')
        self.assertEqual(resp.status_code, 404)

    def test_task_loeschen(self):
        self.client.post('/tasks', json={"title": "Loeschen"})
        resp = self.client.delete('/tasks/1')
        self.assertEqual(resp.status_code, 204)
        # danach darf er nicht mehr da sein
        resp = self.client.get('/tasks/1')
        self.assertEqual(resp.status_code, 404)

    def test_loeschen_nicht_gefunden(self):
        resp = self.client.delete('/tasks/99')
        self.assertEqual(resp.status_code, 404)

    def test_ids_zaehlen_hoch(self):
        r1 = self.client.post('/tasks', json={"title": "A"})
        r2 = self.client.post('/tasks', json={"title": "B"})
        self.assertEqual(r1.get_json()['id'], 1)
        self.assertEqual(r2.get_json()['id'], 2)


if __name__ == '__main__':
    unittest.main()
