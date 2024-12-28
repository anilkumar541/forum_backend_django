from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


# class ForumPagination(PageNumberPagination):
#     page_size = 10  # Adjust the page size as needed
#     page_size_query_param = 'page_size'
#     max_page_size = 50

class ForumPagination(LimitOffsetPagination): 
    # The offset indicates the starting position of the query in relation to the complete set of unpaginated items.   
    # http://127.0.0.1:8000/api/forum/questions/?page_limit=1&page_offset=3
    # here per page you will see one record but the first 3 record to be skipped will show from fourth because page_offset=3


    limit_query_param= "page_limit" #kitna record per page dekhna hai
    offset_query_param= "page_offset" #kha se dekhna hai record

