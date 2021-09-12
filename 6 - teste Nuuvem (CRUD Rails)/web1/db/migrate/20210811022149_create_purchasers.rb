class CreatePurchasers < ActiveRecord::Migration[6.1]
  def change
    create_table :purchasers do |t|
      t.string :name, limit: 255

      t.timestamps
    end
  end
end
