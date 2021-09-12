class CreateSales < ActiveRecord::Migration[6.1]
  def change
    create_table :sales do |t|
      t.integer :purchase_count
      t.references :item, null: false, foreign_key: true
      t.references :merchant, null: false, foreign_key: true
      t.references :purchaser, null: false, foreign_key: true

      t.timestamps
    end
  end
end
