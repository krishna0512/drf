from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^GetCurSet/',         GetCurSet,          name='GetCurSet'        ),
    url(r'^PostCurSet/',        PostCurSet,         name='PostCurSet'       ),
    url(r'^PostTimedSet/',      PostTimedSet,       name='PostTimedSet'     ),
    url(r'^PostQues/',          PostQues,           name='PostQues'         ),
    url(r'^SubAns/',            SubAns,             name='SubAns'           ),
    url(r'^PostInsertQuery/',   PostInsertQuery,    name='PostInsertQuery'  ),
    url(r'^GetInsertQuery/',    GetInsertQuery,     name='GetInsertQuery'   ),
    url(r'^Register/',          Register,           name='Register'         ),
    url(r'^Login/',             Login,              name='Login'            ),
    url(r'^Delete/',            Delete,             name='Delete'           ),
    url(r'^ComDelete/',         ComDelete,          name='ComDelete'        ),
    url(r'^Search/',            Search,             name='Search'           ),
    url(r'^GetUserDetail/',     GetUserDetail,      name='GetUserDetail'    ),
    url(r'^Logout/',            Logout,             name='Logout'           ),
    url(r'^GetLoggedinUsers/',  GetLoggedinUsers,   name='GetLoggedinUsers' ),
    url(r'^GetAllUsers/',       GetAllUsers,        name='GetAllUsers'      )
]
