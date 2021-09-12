# Número de visualizações geradas para cada real investido
views_per_Real = 30

# Número máximo de compartilhamentos por anúncio
share_cap = 4

# Novas views por compartilhamento
new_views_per_share = 40

# Global variables
clicks_per_view = 12/100
shares_per_click = 3/20
shares_per_view = clicks_per_view * shares_per_click
index = shares_per_view * float(new_views_per_share)

def max_clicks(invested_views):
    clicks = max_views(invested_views) * clicks_per_view
    return round(clicks, 2)


def max_shares(invested_views):
    shares = 0

    for i in range(share_cap):
        shares = shares + ((invested_views*(index**i)) * shares_per_view)

    return round(shares, 2)


def max_views(invested_views):
    views = 0

    for i in range(share_cap):
        views = views + (invested_views*(index**(i + 1)))
    
    return round(invested_views + views, 2)