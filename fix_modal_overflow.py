with open('src/app/admin/page.tsx', 'r') as f:
    content = f.read()

# Make the left column a flex container and the player list flex-1
old_col = """              <div className="w-full md:w-1/3 space-y-4">"""
new_col = """              <div className="w-full md:w-1/3 flex flex-col gap-3 h-full max-h-[70vh]">"""
content = content.replace(old_col, new_col)

old_list = """                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-4 max-h-[50vh] overflow-y-auto space-y-2">"""
new_list = """                <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-2xl p-3 flex-1 overflow-y-auto space-y-2 min-h-0">"""
content = content.replace(old_list, new_list)

# Also fix the spacing on the select all buttons which were inside the space-y-4 implicitly
old_select_btns = """                <div className="flex justify-between gap-1 mt-2">"""
new_select_btns = """                <div className="flex justify-between gap-1 shrink-0">"""
content = content.replace(old_select_btns, new_select_btns)

old_courts = """                <div className="flex gap-2">
                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 flex flex-col justify-center">"""
new_courts = """                <div className="flex gap-2 shrink-0">
                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-2 flex flex-col justify-center">"""
content = content.replace(old_courts, new_courts)

old_courts_2 = """                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3 flex flex-col justify-center">"""
new_courts_2 = """                  <div className="flex-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-2 flex flex-col justify-center">"""
content = content.replace(old_courts_2, new_courts_2)

old_cb = """                <div className="flex gap-4 mt-1 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3">"""
new_cb = """                <div className="flex flex-col gap-2 shrink-0 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-xl p-3">"""
content = content.replace(old_cb, new_cb)

old_gen = """                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md mt-2"
                >"""
new_gen = """                <button 
                  onClick={handleGenerate}
                  disabled={isGenerating || selectedPlayerIds.size < 4}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3.5 rounded-xl font-bold flex items-center justify-center gap-2 disabled:opacity-50 transition-all shadow-md shrink-0"
                >"""
content = content.replace(old_gen, new_gen)

with open('src/app/admin/page.tsx', 'w') as f:
    f.write(content)
