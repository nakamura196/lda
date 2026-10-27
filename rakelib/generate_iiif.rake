###############################################################################
# TASK: generate_iiif
#
# create static IIIF Image API level 0 files (fixed sizes and tiles) for the
# spreads in files/original/<issue>/, into objects/iiif/3/<name>/.
# Provided by the static_iiif gem (https://github.com/nakamura196/static_iiif);
# needs the libvips command-line tools (e.g. `brew install vips`).
#
# Every spread is 3680 px on the long side, under the gem's default tile
# threshold (4000 px), so the threshold is lowered to 2000 px: spreads with
# small type are worth deep zoom.
#
# No Image API 2 folders: the site writes version 3 manifests only, and GitHub
# Pages copies every link when it publishes, so they would be a second copy of
# all tiles (the site would be about 930 MB instead of about 600 MB, against a
# 1 GB limit).
#
# The gem's own task reads one folder; the spreads are in one folder per issue,
# so each issue folder is read in turn. <name> is the file name, which already
# carries the issue (yanesen-01-001).
#
# Usage:  rake generate_iiif
#         rake "generate_iiif[true]"   (redo images that are up to date)
###############################################################################

require 'static_iiif'

desc 'Generate static IIIF Image API level 0 files (sizes and tiles) for files/original/<issue>/'
task :generate_iiif, [:force] do |_t, args|
  abort 'generate_iiif: libvips is required (e.g. `brew install vips`).' unless StaticIIIF::Vips.available?

  level0 = StaticIIIF::Level0.new(tile_threshold: 2000)
  output = 'objects/iiif/3'
  Dir.glob('files/original/*/').sort.each do |input|
    level0.generate_dir(input, output, force: args[:force] == 'true') do |src, dir, meta|
      next puts("Skipping: #{dir} is up to date") unless meta

      tiles = meta['tiles'] ? ', tiles' : ''
      puts "Created: #{dir} (#{meta['width']}x#{meta['height']}, #{meta['sizes'].size} sizes#{tiles}) from #{src}"
    end
  end
end
