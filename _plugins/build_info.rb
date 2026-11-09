# frozen_string_literal: true

# Records the commit being built as site.build_commit, for the version shown in the footer.
Jekyll::Hooks.register :site, :after_init do |site|
  commit = begin
    `git rev-parse HEAD 2>/dev/null`.strip
  rescue SystemCallError
    ''
  end
  site.config['build_commit'] = commit unless commit.empty?
end
