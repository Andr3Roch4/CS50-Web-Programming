from django.contrib import admin
from .models import User, Listings, Comments, Bids, Categories, Watchlist

# Register your models here.
admin.site.register(User)
admin.site.register(Listings)
admin.site.register(Comments)
admin.site.register(Bids)
admin.site.register(Categories)
admin.site.register(Watchlist)