require 'csv'

class FrontController < ApplicationController
  def index
  end

  def result

    @file = params[:file]
    @subtotal = 0
    CSV.foreach(@file, :headers => true, :col_sep => "\t", quote_char: nil) do |row|
      Purchaser.create(:name => row['purchaser name'])
      Item.create(:description => row['item description'], :price => row['item price'])
      Merchant.create(:name => row['merchant name'], :adress => row['merchant address'])
      Sale.create(:purchase_count => row['purchase count'], :purchaser_id => Purchaser.last.id, :item_id => Item.last.id, :merchant_id => Merchant.last.id)
      @subtotal += (Sale.last.item.price) * (Sale.last.purchase_count)
    end

    @sales = Sale.all
    @total = 0
    @sales.each do |sale|
      @total += (sale.item.price) * (sale.purchase_count)
    end

  end

end
