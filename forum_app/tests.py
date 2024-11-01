from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Question
from .api.serializers import QuestionSerializer
from django.contrib.auth.models import User

class LikeTests(APITestCase):

    def test_get_like(self):
     url = reverse('like-list')
     response = self.client.get(url)
     self.assertEqual(response.status_code, status.HTTP_200_OK)


class QuestionTests(APITestCase):
   
   def setUp(self):
      self.user = User.objects.create_user(username='testuser', password= 'testpassword')
      self.question = Question.objects.create(title='Test Question', content= 'test content', author= self.user, category='frontend')
      self.client = APIClient()
      self.client.login(username='testuser', password= 'testpassword')

   def test_list_post_question(self):
      url = reverse('question-list')
      data = {
          'title':'Question1',
          'content': '1Content',
          'author':self.user.id,
          'category':'fronted'
      }

      response = self.client.post(url, data, format='json')
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_detail_question(self):
     url = reverse('question-detail', kwargs={'pk': self.question.id})
     response = self.client.get(url)
     self.assertEqual(response.status_code, status.HTTP_200_OK)

     expected_data =QuestionSerializer(self.question).data
     self.assertEqual(response.data, expected_data)
     self.assertDictEqual(response.data, expected_data)
     self.assertJSONEqual(response.content, expected_data)

     self.assertContains(response, 'title')
