Jekyll::Hooks.register :site, :post_write do |site|
    `npm exec -- pagefind --site _site --output-path _site/pagefind`
end
