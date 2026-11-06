-- tog.lua: pandoc Lua filter for the IEEE Transactions on Games version (LaTeX output, IEEEtran).
-- (Lua filters run before --shift-heading-level-by, so these sections are found by their titles, at any level.)
-- 1. The section "Abstract" becomes the IEEEtran abstract; its "**Index Terms:**" paragraph
--    becomes the IEEEkeywords block.
-- 2. The section "References" (paragraphs "[n] entry") becomes a thebibliography list,
--    one \bibitem per entry, in the order given; the class prints the heading.
-- 3. Every figure becomes a figure* float (two-column width) and every table a table* float with
--    its caption above it, as IEEE places them; in one-column mode the class treats the starred
--    floats as ordinary ones. The class numbers them ("Fig. 1", "TABLE I").
-- Float placement is [!t] unless the metadata variable floatpos sets another (the supplement uses !htbp).
-- Figures are drawn at the full text width unless the metadata variable figscale sets a fraction of it.
-- Nothing in the text is changed.

local function latex(inlines)
  return (pandoc.write(pandoc.Pandoc({pandoc.Plain(inlines)}), 'latex'):gsub('%s+$', ''))
end

local function raw(s) return pandoc.RawBlock('latex', s) end

local function header_text(b) return pandoc.utils.stringify(b.content) end

local function figure_block(fig)
  local img
  pandoc.walk_block(fig, {Image = function(i) img = img or i end})
  local cap = {}
  for _, b in ipairs(fig.caption.long) do
    for _, x in ipairs(b.content or {}) do table.insert(cap, x) end
  end
  return raw('\\begin{figure*}[' .. FLOATPOS .. ']\n\\centering\n\\includegraphics[width=' .. FIGWIDTH .. ']{' .. img.src .. '}\n'
             .. '\\caption{' .. latex(cap) .. '}\n\\end{figure*}')
end

local function cell(c)
  local out = {}
  for _, b in ipairs(c) do
    for _, x in ipairs(b.content or {}) do table.insert(out, x) end
  end
  return latex(out)
end

local function table_block(tbl)
  local s = pandoc.utils.to_simple_table(tbl)
  local n = #s.headers
  local spec = {}
  local total = 0
  for _, w in ipairs(s.widths) do total = total + w end
  for i = 1, n do
    if total > 0 then
      spec[i] = string.format('>{\\raggedright\\arraybackslash}p{%.3f\\linewidth}', s.widths[i] / total * 0.97 - 0.012)
    else
      spec[i] = 'l'
    end
  end
  local lines = {}
  local hdr = {}
  for i = 1, n do hdr[i] = '\\textbf{' .. cell(s.headers[i]) .. '}' end
  table.insert(lines, table.concat(hdr, ' & ') .. ' \\\\ \\hline')
  for _, row in ipairs(s.rows) do
    local r = {}
    for i = 1, n do r[i] = cell(row[i]) end
    table.insert(lines, table.concat(r, ' & ') .. ' \\\\')
  end
  local cap = latex(s.caption)
  -- a caption that begins "Table S2a. " (the supplement) keeps that label: the class prints it in place of a number
  local label, rest = cap:match('^Table (S%w+)%.%s+(.*)$')
  local setlabel = ''
  if label then
    cap = rest
    setlabel = '\\renewcommand{\\thetable}{' .. label .. '}\n'
  end
  return raw('\\begin{table*}[' .. FLOATPOS .. ']\n' .. setlabel .. '\\caption{' .. cap .. '}\n\\centering\n\\footnotesize\n'
             .. '\\renewcommand{\\arraystretch}{1.15}\n\\setlength{\\tabcolsep}{4pt}\n'
             .. '\\begin{tabular}{' .. table.concat(spec, '') .. '}\n\\hline\n'
             .. table.concat(lines, '\n') .. '\n\\hline\n\\end{tabular}\n\\end{table*}')
end

FLOATPOS = '!t'
FIGWIDTH = '\\textwidth'

function Pandoc(doc)
  if doc.meta.floatpos then FLOATPOS = pandoc.utils.stringify(doc.meta.floatpos) end
  if doc.meta.figscale then FIGWIDTH = pandoc.utils.stringify(doc.meta.figscale) .. '\\textwidth' end
  local out = {}
  local i = 1
  local blocks = doc.blocks
  while i <= #blocks do
    local b = blocks[i]
    if b.t == 'Header' and header_text(b) == 'Abstract' then
      local abs = {}
      local lvl = b.level
      i = i + 1
      while i <= #blocks and not (blocks[i].t == 'Header' and blocks[i].level <= lvl) do
        local x = blocks[i]
        local first = x.content and x.content[1]
        if x.t == 'Para' and first and first.t == 'Strong' and pandoc.utils.stringify(first) == 'Index Terms:' then
          local kw = {}
          for k = 2, #x.content do table.insert(kw, x.content[k]) end
          while kw[1] and (kw[1].t == 'Space' or kw[1].t == 'SoftBreak') do table.remove(kw, 1) end
          doc.meta.indexterms = pandoc.MetaInlines(kw)
        else
          table.insert(abs, x)
        end
        i = i + 1
      end
      doc.meta.abstract = pandoc.MetaBlocks(abs)
    elseif b.t == 'Header' and header_text(b) == 'References' then
      local items = {}
      local lvl = b.level
      i = i + 1
      while i <= #blocks and not (blocks[i].t == 'Header' and blocks[i].level <= lvl) do
        local x = blocks[i]
        if x.t == 'Para' then
          local first = x.content[1]
          local label = first and first.t == 'Str' and first.text:match('^%[(%d+)%]$')
          if not label then error('reference paragraph without a [n] label: ' .. pandoc.utils.stringify(x)) end
          local rest = {}
          for k = 2, #x.content do table.insert(rest, x.content[k]) end
          while rest[1] and rest[1].t == 'Space' do table.remove(rest, 1) end
          table.insert(items, '\\bibitem{b' .. label .. '}\n' .. latex(rest))
        end
        i = i + 1
      end
      table.insert(out, raw('\\begin{thebibliography}{99}\n' .. table.concat(items, '\n\n') .. '\n\\end{thebibliography}'))
    else
      if b.t == 'Figure' then
        table.insert(out, figure_block(b))
      elseif b.t == 'Table' then
        table.insert(out, table_block(b))
      else
        table.insert(out, b)
      end
      i = i + 1
    end
  end
  doc.blocks = out
  return doc
end
