# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2021_08_11_022211) do

  create_table "items", force: :cascade do |t|
    t.decimal "price", precision: 16, scale: 8
    t.text "description", limit: 1000
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "merchants", force: :cascade do |t|
    t.string "name", limit: 255
    t.string "adress", limit: 255
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "purchasers", force: :cascade do |t|
    t.string "name", limit: 255
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
  end

  create_table "sales", force: :cascade do |t|
    t.integer "purchase_count"
    t.integer "item_id", null: false
    t.integer "merchant_id", null: false
    t.integer "purchaser_id", null: false
    t.datetime "created_at", precision: 6, null: false
    t.datetime "updated_at", precision: 6, null: false
    t.index ["item_id"], name: "index_sales_on_item_id"
    t.index ["merchant_id"], name: "index_sales_on_merchant_id"
    t.index ["purchaser_id"], name: "index_sales_on_purchaser_id"
  end

  add_foreign_key "sales", "items"
  add_foreign_key "sales", "merchants"
  add_foreign_key "sales", "purchasers"
end
