json.extract! sale, :id, :purchase_count, :item_id, :merchant_id, :purchaser_id, :created_at, :updated_at
json.url sale_url(sale, format: :json)
