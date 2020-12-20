import datetime
 
from django.utils.translation import ugettext_lazy
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
from rest_framework import HTTP_HEADER_ENCODING
 
 
# 獲取請求頭資料
def get_authorization_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth
 
 
# 自訂認證方式，這個是後面要添加到設定檔的
class ExpiringTokenAuthentication(BaseAuthentication):
    model = Token
 
    def authenticate(self, request):
        auth = get_authorization_header(request)
        if not auth:
            return None
        try:
            token = auth.decode()
        except UnicodeError:
            msg = ugettext_lazy("Token is invalid")
            raise exceptions.AuthenticationFailed(msg)
 
        return self.authenticate_credentials(token)
 
    def authenticate_credentials(self, key):
        # 嘗試從緩存獲取使用者資料（設置中配置了緩存的可以添加，不加也不影響正常功能）
        token_cache = 'token_' + key
        cache_user = cache.get(token_cache)
        if cache_user:
            return cache_user, cache_user   # 這裡需要返回一個清單或元組，原因不詳
        # 緩存獲取到此為止
 
        # 下面開始獲取請求資訊進行驗證
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed("validate failed")
 
        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("user is locked")
 
        # Token有效期時間判斷（注意時間時區問題）
        # 我在設置裡面設置了時區 USE_TZ = False，如果使用utc這裡需要改變。
        if (datetime.datetime.now() - token.created) > datetime.timedelta(hours=0.1*1):
            raise exceptions.AuthenticationFailed('token expired')
 
        # 加入緩存增加查詢速度，下面和上面是配套的，上面沒有從緩存中讀取，這裡就不用儲存到緩存中了
        if token:
            token_cache = 'token_' + key
            cache.set(token_cache, token.user, 600)
        
        # 返回使用者資料
        return token.user, token
 
    def authenticate_header(self, request):
        return 'Token'
