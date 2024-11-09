<?php
header('Content-Type: application/json'); 
header("Access-Control-Allow-Origin: *");

// السماح بأساليب معينة مثل GET و POST و PUT و DELETE
header("Access-Control-Allow-Methods: GET, POST, OPTIONS");

// السماح برؤوس معينة
header("Access-Control-Allow-Headers: Content-Type, Authorization");
$host = 'pdb1050.awardspace.net'; // تغيير إلى المضيف الخاص بك
$dbname = '4438085_devadnan'; // اسم قاعدة البيانات
$username = '4438085_devadnan'; // اسم المستخدم لقاعدة البيانات
$password = 'Adnan&&123'; // كلمة المرور لقاعدة البيانات

// إنشاء الاتصال
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    // تعيين طريقة التعامل مع الأخطاء
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("فشل الاتصال بقاعدة البيانات: " . $e->getMessage());
}

// دالة لجلب جميع المقاطع الصوتية من قاعدة البيانات
function getAllAudioUrls() {
    global $pdo;
    try {
        // استعلام لجلب جميع روابط المقاطع الصوتية
        $sql = "SELECT episode_id, episode_url FROM episodes ORDER BY episode_id ASC";  // تعديل للاستعلام باستخدام 'episode_id' بدلاً من 'id'
        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        
        // التحقق إذا كانت البيانات موجودة
        if ($stmt->rowCount() > 0) {
            // جلب جميع النتائج
            $results = $stmt->fetchAll(PDO::FETCH_ASSOC);
            return $results; // إرجاع كل المقاطع الصوتية
        } else {
            return null; // في حال عدم العثور على أي مقاطع
        }
    } catch (PDOException $e) {
        return "خطأ في الاستعلام: " . $e->getMessage();
    }
}

// جلب كل المقاطع الصوتية وإعادتها
$episodes = getAllAudioUrls();

if ($episodes) {
    echo json_encode(['episodes' => $episodes]);  // إرجاع النتائج في شكل JSON
} else {
    echo json_encode(['error' => 'لا توجد مقاطع صوتية']);
}

?>
