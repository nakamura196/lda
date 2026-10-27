# frozen_string_literal: true

source 'https://rubygems.org'

# needed for Jekyll
gem 'jekyll'
gem 'webrick'
gem 'logger'
gem 'base64'
gem 'ostruct'

# needed for Rake tasks
gem 'rake'
gem 'csv'
gem 'fileutils'
gem 'mini_magick'
unless Gem.win_platform?
  gem 'image_optim'
  gem 'image_optim_pack'
end

# Japanese/Chinese/Korean search index, built at build time (see cjk_index in _config.yml)
group :jekyll_plugins do
  # Gemfile.lock is not committed in this repo, so allow patch releases only
  gem 'cjk_index', '~> 0.1.0', require: 'cjk_index/jekyll'
  # static IIIF: info.json and the item manifests at build time (see static_iiif: in _config.yml)
  gem 'static_iiif', git: 'https://github.com/nakamura196/static_iiif.git', ref: 'cec422e87192b33c8136c9b6f6fff7a268115d7c', require: 'static_iiif/jekyll'
end

# modern / museum looks and the light/dark switch (see the theme's README)
gem 'cb-museum-theme', git: 'https://github.com/nakamura196/cb-museum-theme.git', ref: '17be794b00e4b4bcbdfb3a67c65c24652c4695b5'
