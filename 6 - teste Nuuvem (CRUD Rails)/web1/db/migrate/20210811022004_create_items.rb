class CreateItems < ActiveRecord::Migration[6.1]
  def change
    create_table :items do |t|
      t.decimal :price, precision: 16, scale: 8
      t.text :description, limit: 1000

      t.timestamps
    end
  end
end
