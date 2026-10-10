with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# First, undo the broken close tag at the end.
content = content.replace("          </>\n        )}\n      </main>\n    </div>\n  );\n}", "      </main>\n    </div>\n  );\n}")

# Now, find where the modal starts:
# {/* --- 대진표 자동 생성 모달 --- */}
modal_start = "{/* --- 대진표 자동 생성 모달 --- */}"

# We want to close the conditional BEFORE the modal starts.
# So replace `modal_start` with `</>)}` + `modal_start`
content = content.replace(modal_start, "          </>\n        )}\n\n        " + modal_start)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
