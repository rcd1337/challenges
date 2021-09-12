class CreateMerchants < ActiveRecord::Migration[6.1]
  def change
    create_table :merchants do |t|
      t.string :name, limit: 255
      t.string :adress, limit: 255

      t.timestamps
    end
  end
end
