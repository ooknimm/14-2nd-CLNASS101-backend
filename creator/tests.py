import json
import io
from unittest       import mock

from django.test    import Client, TransactionTestCase
from django.urls    import reverse
from django.db      import connection

from product.models import MainCategory, SubCategory, Difficulty

class TestFirstTemporaryView(TransactionTestCase):
    
    def setUp(self):
        self.client = Client()

        user_data = {
            'name'     : 'dooly',
            'email'    : 'dooly@naver.com',
            'password' : '1q2w3e4r'
        }

        response = self.client.post(
            '/user/signup',
            user_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 201)

        login_data = {
            'email'    : 'dooly@naver.com',
            'password' : '1q2w3e4r'
        }

        response = self.client.post(
            '/user/login',
            login_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 200)
        
        token = json.loads(response.content)['token']

        self.header = {
            'HTTP_Authorization' : token
        }

        main_categories = MainCategory.objects.create(
            id   = 1,
            name = '크리에이티브'
        )

        sub_categories = SubCategory.objects.create(
            id               = 11,
            main_category_id = 1,
            name             = '데이터/개발'
        )

        difficulty = Difficulty.objects.create(
            name = '초급자'
        )

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate main_categories')
            cursor.execute('truncate sub_categories')
            cursor.execute('truncate difficulties')
            cursor.execute('truncate users')
            cursor.execute('truncate products')
            cursor.execute('truncate temporary_products')
            cursor.execute('truncate temporary_kit_images')
            cursor.execute('truncate temporary_kits')
            cursor.execute('truncate temporary_chapters')
            cursor.execute('truncate temporary_lecture_content_descriptions')
            cursor.execute('truncate temporary_lecture_content_images')
            cursor.execute('truncate temporary_lecture_contents')
            cursor.execute('truncate temporary_lectures')
            cursor.execute('truncate temporary_product_images')
            cursor.execute('set foreign_key_checks=1')
    
    @mock.patch('creator.views.S3FileManager')
    def test_first_temporary_view_create(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url1', 'image_url2']

        url = reverse('first_temporary', args=[1])

        json_data = json.dumps({
            "user_id"         : 1,
            "categoryName"    : "크리에이티브",
            "subCategoryName" : "데이터/개발",
            "difficultyName"  : "초급자",
            "name"            : "강의1",
            "price"           : 10,
            "sale"            : 0.35
            })
        files = [io.BytesIO(b'image1'), io.BytesIO(b'image2')] 
        data = {
            'body'  : json_data,
            'files' : files 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'SUCCESS')

    @mock.patch('creator.views.S3FileManager')
    def test_first_temporary_view_fail_key_error(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url1', 'image_url2']
        
        url = reverse('first_temporary', args=[1])

        json_data = json.dumps({
            "user_id"         : 1,
            "categoryName"    : "크리에이티브",
            "subCategoryName" : "데이터/개발",
            "difficultyName"  : "초급자",
            "name"            : "강의1",
            "price"           : 10
            })
        files = [io.BytesIO(b'image1'), io.BytesIO(b'image2')] 
        data = {
            'body'  : json_data,
            'files' : files 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'KEY_ERROR')

    @mock.patch('creator.views.S3FileManager')
    def test_first_temporary_view_fail_query_not_exist(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url1', 'image_url2']
        
        url = reverse('first_temporary', args=[1])

        json_data = json.dumps({
            "user_id"         : 1,
            "categoryName"    : "크리에이티브",
            "subCategoryName" : "가짜",
            "difficultyName"  : "초급자",
            "name"            : "강의1",
            "price"           : 10,
            "sale"            : 0.35
            })
        files = [io.BytesIO(b'image1'), io.BytesIO(b'image2')] 
        data = {
            'body'  : json_data,
            'files' : files 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'SubCategory matching query does not exist.')

    @mock.patch('creator.views.S3FileManager')
    def test_first_temporary_view_get(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url1', 'image_url2']

        url = reverse('first_temporary', args=[1])

        json_data = json.dumps({
            "user_id"         : 1,
            "categoryName"    : "크리에이티브",
            "subCategoryName" : "데이터/개발",
            "difficultyName"  : "초급자",
            "name"            : "강의1",
            "price"           : 10,
            "sale"            : 0.35
            })
        files = [io.BytesIO(b'image1'), io.BytesIO(b'image2')] 
        data = {
            'body'  : json_data,
            'files' : files 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
    
        response = self.client.get(
            url,
            **self.header
        )

        result = {
            "categories"  : [
                {
                    "id"           : 1,
                    "name"         : "크리에이티브",
                    "subCategories": [
                        {
                            'id'     : 11,
                            'name'   : '데이터/개발'
                        }
                    ]
                }
            ],
            "difficulties" : [
                {
                    "id"     : 1,
                    "name"   : "초급자"
                }
            ],
            "temporaryInformation" : {
                "mainCategoryId" : 1,
                "subCategoryId"  : 11,
                "difficultyId"   : 1,
                "name"           : "강의1",
                "price"          : 10,
                "sale"           : "0.35",
                "images"         : [
                    "https://clnass101.s3.amazonaws.com/image_url1",
                    'https://clnass101.s3.amazonaws.com/image_url2'
                ]
            }
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), result)

class TestSecondTemporaryView(TransactionTestCase):
    @mock.patch('creator.views.S3FileManager')
    def setUp(self, mock_S3FileManager):
        self.client = Client()

        user_data = {
            'name'    : 'dooly',
            'email'   : 'dooly@naver.com',
            'password': '1q2w3e4r'
        }

        response = self.client.post(
            '/user/signup',
            user_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 201)

        login_data = {
            'email'    : 'dooly@naver.com',
            'password' : '1q2w3e4r'
        }

        response = self.client.post(
            '/user/login',
            login_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 200)
        
        token = json.loads(response.content)['token']

        self.header = {
            'HTTP_Authorization': token
        }

        main_categories = MainCategory.objects.create(
            id   = 1,
            name = '크리에이티브'
        )

        sub_categories = SubCategory.objects.create(
            id   = 11,
            name = '데이터/개발'
        )

        difficulty = Difficulty.objects.create(
            name = '초급자'
        )

        mock_S3FileManager().file_upload.side_effect = ['image_url1', 'image_url2']

        url = reverse('first_temporary', args=[1])

        json_data = json.dumps({
            "user_id"         : 1,
            "categoryName"    : "크리에이티브",
            "subCategoryName" : "데이터/개발",
            "difficultyName"  : "초급자",
            "name"            : "강의1",
            "price"           : 10,
            "sale"            : 0.35
            })
        files = [io.BytesIO(b'image1'), io.BytesIO(b'image2')] 
        data  = {
            'body'  : json_data,
            'files' : files 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate main_categories')
            cursor.execute('truncate sub_categories')
            cursor.execute('truncate difficulties')
            cursor.execute('truncate users')
            cursor.execute('truncate products')
            cursor.execute('truncate temporary_products')
            cursor.execute('truncate temporary_kit_images')
            cursor.execute('truncate temporary_kits')
            cursor.execute('truncate temporary_chapters')
            cursor.execute('truncate temporary_lecture_content_descriptions')
            cursor.execute('truncate temporary_lecture_content_images')
            cursor.execute('truncate temporary_lecture_contents')
            cursor.execute('truncate temporary_lectures')
            cursor.execute('truncate temporary_product_images')
            cursor.execute('set foreign_key_checks=1')

    @mock.patch('creator.views.S3FileManager')
    def test_second_temporary_view_create(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url3', 'image_url4']
           
        url = reverse('second_temporary', args=[1])

        json_data = json.dumps({
            "chapters" : [
                {
                    "name"     : "챕터1",
                    "lectures" : [
                        {
                            "name" : "렉처1-1"
                        }
                    ]
                },
                {
                    "name"     : "챕터2",
                    "lectures" : [
                        {
                            "name" : "렉처2-1"
                        }
                    ]
                }
            ]
        })
        files = [io.BytesIO(b'image3'), io.BytesIO(b'image4')] 
        data  = {
            'body'  : json_data,
            'files' : files 
        }
       
        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'SUCCESS')

    @mock.patch('creator.views.S3FileManager')
    def test_second_temporary_view_fail_key_error(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url3', 'image_url4']
           
        url = reverse('second_temporary', args=[1])

        json_data = json.dumps({
            "chapters" : [
                {
                    "name"     : "챕터1",
                    "lectures" : [
                        {
                            "name" : "렉처1-1"
                        }
                    ]
                },
                {
                    "name" : "챕터2"
                }
            ]
        })
        files = [io.BytesIO(b'image3'), io.BytesIO(b'image4')] 
        data  = {
            'body'  : json_data,
            'files' : files 
        }
       
        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'KEY_ERROR')

    @mock.patch('creator.views.S3FileManager')
    def test_second_temporary_view_temporary_product_does_not_exist(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url3', 'image_url4']
           
        url = reverse('second_temporary', args=[100])

        json_data = json.dumps({
            "chapters" : [
                {
                    "name"     : "챕터1",
                    "lectures" : [
                        {
                            "name" : "렉처1-1"
                        }
                    ]
                },
                {
                    "name"     : "챕터2",
                    "lectures" : [
                        {
                            "name" : "렉처2-1"
                        }
                    ]
                }
            ]
        })
        files = [io.BytesIO(b'image3'), io.BytesIO(b'image4')] 
        data  = {
            'body' : json_data,
            'files': files 
        }
       
        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)['message'], 'TEMPORARY_PRODUCT_DOES_NOT_EXIST') 

    @mock.patch('creator.views.S3FileManager')
    def test_second_temporary_view_get(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url3', 'image_url4']
           
        url = reverse('second_temporary', args=[1])

        json_data = json.dumps({
            "chapters" : [
                {
                    "name"     : "챕터1",
                    "lectures" : [
                        {
                            "name"  : "렉처1-1"
                        },
                        {
                            "name"  : "렉처1-2"
                        }
                    ]
                },
                {
                    "name"     : "챕터2",
                    "lectures" : [
                        {
                            "name"  : "렉처2-1"
                        }
                    ]
                }
            ]
        })
        files = [io.BytesIO(b'image3'), io.BytesIO(b'image4')] 
        data  = {
            'body' : json_data,
            'files': files 
        }
       
        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url,
            **self.header
        )

        result = {
            "chapters" : [
                {
                    "chapterId" : 1,
                    "name"      : "챕터1",
                    "mainImage" : "https://clnass101.s3.amazonaws.com/image_url3",
                    "lectures"  : [
                        {
                            "name"  : "렉처1-1",
                            "order" : 1
                        },
                        {
                            "name"  : "렉처1-2",
                            "order" : 2
                        }
                    ]
                },
                {
                    "chapterId" : 2,
                    "name"      : "챕터2",
                    "mainImage" : "https://clnass101.s3.amazonaws.com/image_url4",
                    "lectures"  : [
                        {
                            "name"  : "렉처2-1",
                            "order" : 1
                        }
                    ]
                }
            ]
        } 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), result)

class TestThirdTemporaryView(TransactionTestCase):
    @mock.patch('creator.views.S3FileManager')
    def setUp(self, mock_S3FileManager):
        self.client = Client()

        user_data = {
            'name'     : 'dooly',
            'email'    : 'dooly@naver.com',
            'password' : '1q2w3e4r'
        }

        response = self.client.post(
            '/user/signup',
            user_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 201)

        login_data = {
            'email'    : 'dooly@naver.com',
            'password' : '1q2w3e4r'
        }

        response = self.client.post(
            '/user/login',
            login_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 200)
        
        token = json.loads(response.content)['token']

        self.header = {
            'HTTP_Authorization': token
        }

        main_categories = MainCategory.objects.create(
            id   = 1,
            name = '크리에이티브'
        )

        sub_categories = SubCategory.objects.create(
            id   = 11,
            name = '데이터/개발'
        )

        difficulty = Difficulty.objects.create(
            name = '초급자'
        )

        mock_S3FileManager().file_upload.side_effect = ['image_url1', 'image_url2']

        url = reverse('first_temporary', args=[1])

        json_data = json.dumps({
            "user_id"         : 1,
            "categoryName"    : "크리에이티브",
            "subCategoryName" : "데이터/개발",
            "difficultyName"  : "초급자",
            "name"            : "강의1",
            "price"           : 10,
            "sale"            : 0.35
            })
        files = [io.BytesIO(b'image1'), io.BytesIO(b'image2')] 
        data  = {
            'body'  : json_data,
            'files' : files 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
        
        mock_S3FileManager().file_upload.side_effect = ['image_url3', 'image_url4']
           
        url = reverse('second_temporary', args=[1])

        json_data = json.dumps({
            "chapters" : [
                {
                    "name"     : "챕터1",
                    "lectures" : [
                        {
                            "name" : "렉처1-1"
                        }
                    ]
                },
                {
                    "name"     : "챕터2",
                    "lectures" : [
                        {
                            "name" : "렉처2-1"
                        }
                    ]
                }
            ]
        })
        files = [io.BytesIO(b'image3'), io.BytesIO(b'image4')] 
        data  = {
            'body'  : json_data,
            'files' : files 
        }
       
        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate main_categories')
            cursor.execute('truncate sub_categories')
            cursor.execute('truncate difficulties')
            cursor.execute('truncate users')
            cursor.execute('truncate products')
            cursor.execute('truncate temporary_products')
            cursor.execute('truncate temporary_kit_images')
            cursor.execute('truncate temporary_kits')
            cursor.execute('truncate temporary_chapters')
            cursor.execute('truncate temporary_lecture_content_descriptions')
            cursor.execute('truncate temporary_lecture_content_images')
            cursor.execute('truncate temporary_lecture_contents')
            cursor.execute('truncate temporary_lectures')
            cursor.execute('truncate temporary_product_images')
            cursor.execute('set foreign_key_checks=1')
    
    @mock.patch('creator.views.S3FileManager')
    def test_third_temporary_view_create(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = [
            'video_url1',
            'image_url5',
            'image_url6',
            'video_url2',
            'image_url7'
        ]
        url = reverse('third_temporary', args=[1])

        json_data = json.dumps({
            "lectures" : [
                {
                    "lecture_id" : 1,
                    "contents"   : [
                        {
                            "description" : "아무말1-1"
                        },
                        {
                            "description" : "아무말1-2"
                        }
                    ]
                },
                {
                    "lecture_id" : 2,
                    "contents"   : [
                        {
                            "description" : "아무말2-1"
                        }
                    ]
                }
            ]
        })
        images = [
            io.BytesIO(b'image5'),
            io.BytesIO(b'image6'),
            io.BytesIO(b'image7') 
        ]
        videos = [
            io.BytesIO(b'video1'),
            io.BytesIO(b'video2')
        ]
        data = {
            'body'   : json_data,
            'images' : images,
            'videos' : videos 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'SUCCESS')
    
    @mock.patch('creator.views.S3FileManager')
    def test_third_temporary_view_fail_key_error(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = [
            'video_url1',
            'image_url5',
            'image_url6',
            'video_url2',
            'image_url7'
        ]
        url = reverse('third_temporary', args=[1])

        json_data = json.dumps({
            "lectures" : [
                {
                    "lecture_id" : 1,
                    "contents"   : [
                        {
                            "description" : "아무말1-1"
                        },
                        {
                            "description" : "아무말1-2"
                        }
                    ]
                },
                {
                    "lecture_id" : 2
                }
            ]
        })
        images = [
            io.BytesIO(b'image5'),
            io.BytesIO(b'image6'),
            io.BytesIO(b'image7') 
        ]
        videos = [
            io.BytesIO(b'video1'),
            io.BytesIO(b'video2')
        ]
        data = {
            'body'   : json_data,
            'images' : images,
            'videos' : videos 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'KEY_ERROR')

    @mock.patch('creator.views.S3FileManager')
    def test_third_temporary_view_fail_temporary_product_does_not_exist(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = [
            'video_url1',
            'image_url5',
            'image_url6',
            'video_url2',
            'image_url7'
        ]
        url = reverse('third_temporary', args=[100])

        json_data = json.dumps({
            "lectures" : [
                {
                    "lecture_id" : 1,
                    "contents"   : [
                        {
                            "description" : "아무말1-1"
                        },
                        {
                            "description" : "아무말1-2"
                        }
                    ]
                },
                {
                    "lecture_id" : 2,
                    "contents"   : [
                        {
                            "description" : "아무말2-1"
                        }
                    ]
                }
            ]
        })
        images = [
            io.BytesIO(b'image5'),
            io.BytesIO(b'image6'),
            io.BytesIO(b'image7') 
        ]
        videos = [
            io.BytesIO(b'video1'),
            io.BytesIO(b'video2')
        ]
        data = {
            'body'   : json_data,
            'images' : images,
            'videos' : videos 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)['message'], 'TEMPORARY_PRODUCT_DOES_NOT_EXIST')

    @mock.patch('creator.views.S3FileManager')
    def test_third_temporary_view_get(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = [
            'video_url1',
            'image_url5',
            'image_url6',
            'video_url2',
            'image_url7'
        ]
        url = reverse('third_temporary', args=[1])

        json_data = json.dumps({
            "lectures" : [
                {
                    "lecture_id" : 1,
                    "contents"   : [
                        {
                            "description" : "아무말1-1"
                        },
                        {
                            "description" : "아무말1-2"
                        }
                    ]
                },
                {
                    "lecture_id" : 2,
                    "contents"   : [
                        {
                            "description" : "아무말2-1"
                        }
                    ]
                }
            ]
        })
        images = [
            io.BytesIO(b'image5'),
            io.BytesIO(b'image6'),
            io.BytesIO(b'image7') 
        ]
        videos = [
            io.BytesIO(b'video1'),
            io.BytesIO(b'video2')
        ]
        data = {
            'body'   : json_data,
            'images' : images,
            'videos' : videos 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url,
            **self.header
        )

        result = {
            "products" : [
                {
                    "chapter_id"   : 1,
                    "chapterName"  : "챕터1",
                    "chapterOrder" : 1,
                    "lectures"     : [
                        {
                            "lecture_id" : 1,
                            "name"       : "렉처1-1",
                            "videoUrl"   : "https://clnass101.s3.amazonaws.com/video_url1",
                            "order"      : 1,
                            "content"    : [
                                {
                                    "image"       : "https://clnass101.s3.amazonaws.com/image_url5",
                                    "description" : "아무말1-1",
                                    "order"       : 1
                                },
                                {
                                    "image"       : "https://clnass101.s3.amazonaws.com/image_url6",
                                    "description" : "아무말1-2",
                                    "order"       : 2
                                }
                            ]
                        }
                    ]
                },
                {
                    "chapter_id"   : 2,
                    "chapterName"  : "챕터2",
                    "chapterOrder" : 2,
                    "lectures"     : [
                        {
                            "lecture_id" : 2,
                            "name"       : "렉처2-1",
                            "videoUrl"   : "https://clnass101.s3.amazonaws.com/video_url2",
                            "order"      : 1,
                            "content"    : [
                                {
                                    "image"       : "https://clnass101.s3.amazonaws.com/image_url7",
                                    "description" : "아무말2-1",
                                    "order"       : 1
                                },
                            ]
                        }
                    ]
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), result)


class TestFourthTemporaryView(TransactionTestCase):
    @mock.patch('creator.views.S3FileManager')
    def setUp(self, mock_S3FileManager):
        self.client = Client()

        user_data = {
            'name'     : 'dooly',
            'email'    : 'dooly@naver.com',
            'password' : '1q2w3e4r'
        }

        response = self.client.post(
            '/user/signup',
            user_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 201)

        login_data = {
            'email': 'dooly@naver.com',
            'password': '1q2w3e4r'
        }

        response = self.client.post(
            '/user/login',
            login_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 200)
        
        token = json.loads(response.content)['token']

        self.header = {
            'HTTP_Authorization' : token
        }

        main_categories = MainCategory.objects.create(
            id   = 1,
            name = '크리에이티브'
        )

        sub_categories = SubCategory.objects.create(
            id   = 11,
            name = '데이터/개발'
        )

        difficulty = Difficulty.objects.create(
            name = '초급자'
        )

        mock_S3FileManager().file_upload.side_effect = ['image_url1', 'image_url2']

        url = reverse('first_temporary', args=[1])

        json_data = json.dumps({
            "user_id"         : 1,
            "categoryName"    : "크리에이티브",
            "subCategoryName" : "데이터/개발",
            "difficultyName"  : "초급자",
            "name"            : "강의1",
            "price"           : 10,
            "sale"            : 0.35
            })
        files = [io.BytesIO(b'image1'), io.BytesIO(b'image2')] 
        data  = {
            'body'  : json_data,
            'files' : files 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
        
        mock_S3FileManager().file_upload.side_effect = ['image_url3', 'image_url4']
           
        url = reverse('second_temporary', args=[1])

        json_data = json.dumps({
            "chapters" : [
                {
                    "name"     : "챕터1",
                    "lectures" : [
                        {
                            "name" : "렉처1-1"
                        }
                    ]
                },
                {
                    "name"     : "챕터2",
                    "lectures" : [
                        {
                            "name" : "렉처2-1"
                        }
                    ]
                }
            ]
        })
        files = [io.BytesIO(b'image3'), io.BytesIO(b'image4')] 
        data  = {
            'body'  : json_data,
            'files' : files 
        }
       
        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
        
        mock_S3FileManager().file_upload.side_effect = [
            'video_url1',
            'image_url5',
            'image_url6',
            'video_url2',
            'image_url7'
        ]
        url = reverse('third_temporary', args=[1])

        json_data = json.dumps({
            "lectures" : [
                {
                    "lecture_id" : 1,
                    "contents"   : [
                        {
                            "description" : "아무말1-1"
                        },
                        {
                            "description" : "아무말1-2"
                        }
                    ]
                },
                {
                    "lecture_id" : 2,
                    "contents"   : [
                        {
                            "description" : "아무말2-1"
                        }
                    ]
                }
            ]
        })
        images = [
            io.BytesIO(b'image5'),
            io.BytesIO(b'image6'),
            io.BytesIO(b'image7') 
        ]
        videos = [
            io.BytesIO(b'video1'),
            io.BytesIO(b'video2')
        ]
        data = {
            'body'   : json_data,
            'images' : images,
            'videos' : videos 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate main_categories')
            cursor.execute('truncate sub_categories')
            cursor.execute('truncate difficulties')
            cursor.execute('truncate users')
            cursor.execute('truncate products')
            cursor.execute('truncate temporary_products')
            cursor.execute('truncate temporary_kit_images')
            cursor.execute('truncate temporary_kits')
            cursor.execute('truncate temporary_chapters')
            cursor.execute('truncate temporary_lecture_content_descriptions')
            cursor.execute('truncate temporary_lecture_content_images')
            cursor.execute('truncate temporary_lecture_contents')
            cursor.execute('truncate temporary_lectures')
            cursor.execute('truncate temporary_product_images')
            cursor.execute('set foreign_key_checks=1')
    
    @mock.patch('creator.views.S3FileManager')
    def test_fourth_temporary_view_create(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url8', 'image_url9']

        url = reverse('fourth_temporary', args=[1])
        json_data = json.dumps({
            "kits" : [
                {
                    "name" : "키트1"
                },
                {
                    "name" : "키트2"
                }
            ]
        })
        files = [io.BytesIO(b'image8'), io.BytesIO(b'image9')]
        data = {
            'body'  : json_data,
            'files' : files
        }
        
        response = self.client.post(
            url,
            data,
            **self.header
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'SUCCESS')

    @mock.patch('creator.views.S3FileManager')
    def test_fourth_temporary_view_fail_key_error(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url8', 'image_url9']

        url = reverse('fourth_temporary', args=[1])

        files = [io.BytesIO(b'image8'), io.BytesIO(b'image9')]
        data = {
            'files' : files
        }
        
        response = self.client.post(
            url,
            data,
            **self.header
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['message'], 'KEY_ERROR')

    @mock.patch('creator.views.S3FileManager')
    def test_fourth_temporary_view_fail_temporary_prouct_does_not_exist(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url8', 'image_url9']

        url = reverse('fourth_temporary', args=[100])
        json_data = json.dumps({
            "kits" : [
                {
                    "name" : "키트1"
                },
                {
                    "name" : "키트2"
                }
            ]
        })
        files = [io.BytesIO(b'image8'), io.BytesIO(b'image9')]
        data = {
            'body'  : json_data,
            'files' : files
        }
        
        response = self.client.post(
            url,
            data,
            **self.header
        )
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)['message'], 'TEMPORARY_PRODUCT_DOES_NOT_EXIST')

    @mock.patch('creator.views.S3FileManager')
    def test_fourth_temporary_view_get(self, mock_S3FileManager):
        mock_S3FileManager().file_upload.side_effect = ['image_url8', 'image_url9']

        url = reverse('fourth_temporary', args=[1])
        json_data = json.dumps({
            "kits" : [
                {
                    "name" : "키트1"
                },
                {
                    "name" : "키트2"
                }
            ]
        })
        files = [io.BytesIO(b'image8'), io.BytesIO(b'image9')]
        data = {
            'body'  : json_data,
            'files' : files
        }
        
        response = self.client.post(
            url,
            data,
            **self.header
        )
        
        self.assertEqual(response.status_code, 200)

        response = self.client.get(
            url,
            **self.header
        )

        result = {
            "kits" : [
                {
                    "id"        : 1,
                    "name"      : "키트1",
                    "imageUrls" : [
                        "https://clnass101.s3.amazonaws.com/image_url8"
                    ]
                },
                {
                    "id"        : 2,
                    "name"      : "키트2",
                    "imageUrls" : [
                        "https://clnass101.s3.amazonaws.com/image_url9"
                    ]
                }
            ]
        }
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), result)

class TestTemporaryProductCreate(TransactionTestCase):
    @mock.patch('creator.views.S3FileManager')
    def setUp(self, mock_S3FileManager):
        self.client = Client()

        user_data = {
            'name'     : 'dooly',
            'email'    : 'dooly@naver.com',
            'password' : '1q2w3e4r'
        }

        response = self.client.post(
            '/user/signup',
            user_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 201)

        login_data = {
            'email'    : 'dooly@naver.com',
            'password' : '1q2w3e4r'
        }

        response = self.client.post(
            '/user/login',
            login_data,
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 200)
        
        token = json.loads(response.content)['token']

        self.header = {
            'HTTP_Authorization' : token
        }

        main_categories = MainCategory.objects.create(
            id   = 1,
            name = '크리에이티브'
        )

        sub_categories = SubCategory.objects.create(
            id   = 11,
            name = '데이터/개발'
        )

        difficulty = Difficulty.objects.create(
            name = '초급자'
        )

        mock_S3FileManager().file_upload.side_effect = ['image_url1', 'image_url2']

        url = reverse('first_temporary', args=[1])

        json_data = json.dumps({
            "user_id"         : 1,
            "categoryName"    : "크리에이티브",
            "subCategoryName" : "데이터/개발",
            "difficultyName"  : "초급자",
            "name"            : "강의1",
            "price"           : 10,
            "sale"            : 0.35
            })
        files = [io.BytesIO(b'image1'), io.BytesIO(b'image2')] 
        data = {
            'body'  : json_data,
            'files' : files 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
        
        mock_S3FileManager().file_upload.side_effect = ['image_url3', 'image_url4']
           
        url = reverse('second_temporary', args=[1])

        json_data = json.dumps({
            "chapters" : [
                {
                    "name"     : "챕터1",
                    "lectures" : [
                        {
                            "name" : "렉처1-1"
                        }
                    ]
                },
                {
                    "name"     : "챕터2",
                    "lectures" : [
                        {
                            "name" : "렉처2-1"
                        }
                    ]
                }
            ]
        })
        files = [io.BytesIO(b'image3'), io.BytesIO(b'image4')] 
        data = {
            'body'  : json_data,
            'files' : files 
        }
       
        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)
        
        mock_S3FileManager().file_upload.side_effect = [
            'video_url1',
            'image_url5',
            'image_url6',
            'video_url2',
            'image_url7'
        ]
        url = reverse('third_temporary', args=[1])

        json_data = json.dumps({
            "lectures" : [
                {
                    "lecture_id" : 1,
                    "contents"   : [
                        {
                            "description" : "아무말1-1"
                        },
                        {
                            "description" : "아무말1-2"
                        }
                    ]
                },
                {
                    "lecture_id" : 2,
                    "contents"   : [
                        {
                            "description" : "아무말2-1"
                        }
                    ]
                }
            ]
        })
        images = [
            io.BytesIO(b'image5'),
            io.BytesIO(b'image6'),
            io.BytesIO(b'image7') 
        ]
        videos = [
            io.BytesIO(b'video1'),
            io.BytesIO(b'video2')
        ]
        data = {
            'body'   : json_data,
            'images' : images,
            'videos' : videos 
        }

        response = self.client.post(
            url,
            data,
            **self.header
        )

        self.assertEqual(response.status_code, 200)

        mock_S3FileManager().file_upload.side_effect = ['image_url8', 'image_url9']

        url = reverse('fourth_temporary', args=[1])
        json_data = json.dumps({
            "kits" : [
                {
                    "name" : "키트1"
                },
                {
                    "name" : "키트2"
                }
            ]
        })
        files = [io.BytesIO(b'image8'), io.BytesIO(b'image9')]
        data = {
            'body'  : json_data,
            'files' : files
        }
        
        response = self.client.post(
            url,
            data,
            **self.header
        )
        
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute('set foreign_key_checks=0')
            cursor.execute('truncate main_categories')
            cursor.execute('truncate sub_categories')
            cursor.execute('truncate difficulties')
            cursor.execute('truncate users')
            cursor.execute('truncate products')
            cursor.execute('truncate temporary_products')
            cursor.execute('truncate temporary_kit_images')
            cursor.execute('truncate temporary_kits')
            cursor.execute('truncate temporary_chapters')
            cursor.execute('truncate temporary_lecture_content_descriptions')
            cursor.execute('truncate temporary_lecture_content_images')
            cursor.execute('truncate temporary_lecture_contents')
            cursor.execute('truncate temporary_lectures')
            cursor.execute('truncate temporary_product_images')
            cursor.execute('set foreign_key_checks=1')

    @mock.patch('creator.views.S3FileManager')
    def test_temporary_product_create(self, mock_S3FileManager):
        url = reverse('create_temporary', args=[1])
        response = self.client.post(
            url,
            **self.header
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content)['message'], 'SUCCESS')

    @mock.patch('creator.views.S3FileManager')
    def test_temporary_product_create_fail_temporary_product_does_not_exist(self, mock_S3FileManager):
        url = reverse('create_temporary', args=[100])
        response = self.client.post(
            url,
            **self.header
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.content)['message'], 'TEMPORARY_PRODUCT_DOES_NOT_EXIST')
