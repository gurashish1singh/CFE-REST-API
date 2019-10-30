# To test API automatically

from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status

from rest_framework_jwt.settings import api_settings
payload_handler =  api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

from postings.models import BlogPost

User = get_user_model()

class BlogPostAPITestCase(APITestCase):
    def setUp(self):
        user_obj = User(
            username='TestUser', 
            email = 'test@test.com'
            )
        user_obj.set_password('RandomTest')
        user_obj.save()

        blog_post = BlogPost.objects.create(
            user=user_obj, 
            title='Test Title', 
            content='This is a test of the API'
            )

    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count,1)


    def test_single_post(self):
        post_count = BlogPost.objects.count()
        self.assertEqual(post_count,1)

    # Tested the get_list
    def test_get_list(self):
        data = {}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)


    # Tested the create item
    def test_post_item(self):
        data = {'title':'Testing create method', 'content':'Testing create content'}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        # print(response.data)
    


    # Tested the get_list item
    def test_get_item(self):
        blog_post = BlogPost.objects.first()
        data = {}
        url = blog_post.get_api_url()
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)


    # Tested the Update item
    def test_update_item(self):
        blog_post = BlogPost.objects.first()
        url = blog_post.get_api_url()
        data = {'title':'Testing update method', 'content':'Testing update content'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    # Tested the Update item with authentication
    def test_update_item_with_user(self):
        blog_post = BlogPost.objects.first()
        # print(blog_post.content)
        url = blog_post.get_api_url()
        data = {'title':'Testing update method', 'content':'Testing update content'}
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>   
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)


    # Tested the create item with authentication
    def test_post_item_with_user(self):
        user_obj = User.objects.first()
        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>   
        data = {'title':'Testing create method with authentication', 'content':'Testing create content with authentication'}
        url = api_reverse('api-postings:post-listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)


    # Tested user ownership 
    def test_user_ownership(self):
        owner = User.objects.create(username='TestUser2')
        blog_post = BlogPost.objects.create(
            user=owner, 
            title='Test Title of Owner', 
            content='This is a test of Ownership'
            )

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.username, owner.username)

        payload = payload_handler(user_obj)
        token_rsp = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp) # JWT <token>   
        
        url = blog_post.get_api_url()
        data = {'title':'Testing ownership', 'content':'Testing ownership content'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # print(response.data)