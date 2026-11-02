-- ki.lua -- pandoc filter for docs/manuscript_ki/manuscript_ki.md and supplement_ki.md.
-- The section headed "Abstract" (a level-2 heading in the source) is taken out of the body and put
-- into the metadata field "abstract", and its line "**Keywords:** a; b; c" into the list "keywords",
-- so that the template can set them in the abstract environment of svjour3.  Nothing else changes.

-- A full 40-character commit hash cannot break at the end of a line in a two-column page; allow a
-- break (without a hyphen) after every eighth character.  The characters themselves are unchanged.
function Str(el)
  local h, rest = el.text:match("^(%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x%x)(%p*)$")
  if h and FORMAT:match("latex") then
    local parts = {}
    for i = 1, #h, 8 do
      table.insert(parts, h:sub(i, i + 7))
    end
    return pandoc.RawInline("latex", table.concat(parts, "\\allowbreak{}") .. rest)
  end
end

local function is_abstract_header(b)
  return b.t == "Header" and b.level == 2 and pandoc.utils.stringify(b.content) == "Abstract"
end

function Pandoc(doc)
  local body, abstract, keywords = {}, {}, {}
  local inside = false
  for _, b in ipairs(doc.blocks) do
    if is_abstract_header(b) then
      inside = true
    elseif inside and b.t == "Header" and b.level <= 2 then
      inside = false
      table.insert(body, b)
    elseif inside then
      local s = pandoc.utils.stringify(b)
      local kw = s:match("^Keywords:%s*(.*)$")
      if kw then
        for k in kw:gmatch("[^;]+") do
          local kk = k:gsub("^%s+", "")
          kk = kk:gsub("%s+$", "")
          table.insert(keywords, pandoc.MetaInlines(pandoc.Inlines(kk)))
        end
      else
        table.insert(abstract, b)
      end
    else
      table.insert(body, b)
    end
  end
  if #abstract > 0 then
    doc.meta.abstract = pandoc.MetaBlocks(abstract)
  end
  if #keywords > 0 then
    doc.meta.keywords = pandoc.MetaList(keywords)
  end
  doc.blocks = body
  return doc
end
