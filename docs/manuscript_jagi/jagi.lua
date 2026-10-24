-- jagi.lua -- pandoc filter for the JAGI build.
-- The kit sets the word "Abstract" as a centered title in its own style (Abstract Title), not as
-- a section heading. This filter turns the heading "Abstract" into a paragraph in that style.
-- Nothing else is changed.
function Header(h)
  if pandoc.utils.stringify(h) == "Abstract" then
    return pandoc.Div({pandoc.Para(h.content)}, {["custom-style"] = "Abstract Title"})
  end
end
