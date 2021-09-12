Rails.application.routes.draw do
  resources :sales
  
  root "front#index"
  get 'front/index'

  post 'result', to: "front#result"
  get 'result', to: redirect('')
  # For details on the DSL available within this file, see https://guides.rubyonrails.org/routing.html
end
